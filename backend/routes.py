from flask import jsonify, request, render_template, send_from_directory
from .models import Item, Message, MessageCreateSchema, ItemCreate, ItemUpdate
from sqlalchemy.exc import SQLAlchemyError
# appオブジェクトを直接インポートしようとすると、循環参照の問題が発生したり、アプリケーションの構造が複雑になったりすることがあります。
# current_appを使うことで、　循環参照を起こさずに、どこからでも現在のアプリケーションインスタンスにアクセスできる便利な方法を提供します。
from sqlalchemy import desc, or_
from flask import current_app # ログ出力用
from pydantic import ValidationError
from .config import photos
import os
import time


def register_routes(app, get_db):

    # Vue.jsのSPAをサーブするためのルート
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')





# 全てのアイテムを取得するエンドポイント (GET)
    @app.route('/api/items', methods=['GET'])
    def get_items():
        try:
            db = get_db()
            items = db.query(Item).order_by(desc(Item.updated_at)).all()
            return jsonify([item.to_dict() for item in items]), 200

        except SQLAlchemyError as e: # DB関連の具体的なエラー
            current_app.logger.error(f"Database error retrieving items: {e}", exc_info=True) # メッセージを具体的に
            return jsonify({'error': 'A database error occurred. Please try again later.'}), 500 # ユーザー向けメッセージ

        except Exception as e:
            # これがキャッチされるのは、SQLAlchemyError以外の予期せぬPythonエラー
            current_app.logger.error(f"An unexpected error occurred while retrieving items: {e}", exc_info=True)
            return jsonify({"error": "An unexpected server error occurred."}), 500


    @app.route('/api/items/search', methods=['GET'])
    def search_items():
        try:
            query = request.args.get('q', '').strip()

            if not query:
                return jsonify({'error': 'Query parameter "q" is required.'}), 400

            db = get_db()
            items = db.query(Item).filter(
                or_(
                    Item.name.ilike(f'%{query}%'),
                    Item.category.ilike(f'%{query}%'),
                    Item.description.ilike(f'%{query}%'),
                )
            ).order_by(desc(Item.updated_at)).all()

            return jsonify([item.to_dict() for item in items]), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during search: {e}", exc_info=True)
            return jsonify({'error': 'A database error occurred during search.'}), 500

        except Exception as e:
            current_app.logger.error(f"Unexpected error during search: {e}", exc_info=True)
            return jsonify({"error": "An unexpected server error occurred during search."}), 500



# 特定のアイテムを取得するエンドポイント (GET)。　Flaskが自動的にitem_idを整数に変換してくれます。
    @app.route('/api/item/<int:item_id>', methods=['GET'])
    def get_item(item_id: int):
        time.sleep(0.3)
        try:
            db = get_db()
            item = db.query(Item).filter(Item.id == item_id).first()
            if item is None:
                return jsonify({"error": "Item not found"}), 404
            return jsonify(item.to_dict()), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error retrieving the item: {e}", exc_info=True) # メッセージを具体的に
            return jsonify({'error': 'A database error occurred. Please try again later.'}), 500 # ユーザー向けメッセージ

        except Exception as e:
            # これがキャッチされるのは、SQLAlchemyError以外の予期せぬPythonエラー
            current_app.logger.error(f"An unexpected error occurred while retrieving the item: {e}", exc_info=True)
            return jsonify({"error": "An unexpected server error occurred."}), 500



# アイテムを作成するためのエンドポイント
    @app.route('/api/admin/create-item', methods=['POST'])
    def create_item():
        # 1. ファイルの存在チェックと初期検証
        # リクエストが 'multipart/form-data' であることを想定
        if 'image' not in request.files:
            current_app.logger.warning("No 'image' file part in the request.")
            return jsonify({'error': 'There is no image file selected.'}), 400

        file = request.files['image']

        if file.filename == '':
            current_app.logger.warning("No selected file for 'image'. filename is empty.")
            return jsonify({'error': 'There is no image file selected.'}), 400

        # 2. テキストデータ（フォームフィールド）のPydanticバリデーション
        # request.form は ImmutableMultiDict なので、辞書に変換してPydanticに渡す
        item_data_from_form = request.form.to_dict()

        try:
            # Pydanticモデルで入力データをバリデーション
            # image_url と image_filename は、この時点ではまだファイル保存前なので、
            # Pydanticモデルの Optional なフィールドとして自動的に None が扱われる。
            validated_data = ItemCreate(**item_data_from_form)
            current_app.logger.info("Pydantic validation successful.")
        except ValidationError as e:
            current_app.logger.error(f"Pydantic validation error for create_item: {e.errors()}")
            # PydanticエラーメッセージをJSON形式で返す
            return jsonify({'error': e.errors()}), 400
        except Exception as e:
            # Pydanticモデルのインスタンス化中に発生する予期せぬエラー
            current_app.logger.error(f"Unexpected error during Pydantic model creation: {e}", exc_info=True)
            return jsonify({'error': 'リクエストデータの処理中に予期せぬエラーが発生しました。'}), 400

        # 3. ファイルの保存
        # Pydanticバリデーション成功後にファイルを保存する
        saved_filename = None # DB保存失敗時にファイルを削除するために保持
        try:
            saved_filename = photos.save(file)
            image_url = photos.url(saved_filename)
            current_app.logger.info(f"Image saved: {saved_filename}, URL: {image_url}")
        except Exception as e:
            current_app.logger.error(f"Error saving image file: {e}", exc_info=True)
            return jsonify({'error': '写真ファイルの保存に失敗しました。'}), 500

        db = None # tryブロック外でdbを初期化 (エラーハンドリングのため)
        try:
            db = get_db()

            # Pydanticのバリデーション済みデータと画像情報を結合してSQLAlchemyのItemインスタンスを作成
            item_dict = validated_data.model_dump() # Pydanticモデルを辞書に変換
            item_dict['image_filename'] = saved_filename
            item_dict['image_url'] = image_url

            new_item = Item(**item_dict)

            db.add(new_item)
            db.commit() # commit時に自動的に内部で flush() が実行されるため、idが生成される

            current_app.logger.info(f"Item created successfully with ID: {new_item.id}")
            result = new_item.to_dict()
            return jsonify(result), 201

        except SQLAlchemyError as e:
            if db:
                db.rollback() # DBエラーの場合はロールバック
            current_app.logger.error(f"Database error saving item: {e}", exc_info=True)
            # DB保存に失敗した場合、保存したファイルを削除して孤立ファイルを防ぐ
            if saved_filename:
                file_path_to_remove = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], saved_filename)
                try:
                    if os.path.exists(file_path_to_remove):
                        os.remove(file_path_to_remove)
                        current_app.logger.info(f"Successfully removed orphaned file: {saved_filename}")
                except Exception as file_e:
                    current_app.logger.error(f"Error deleting orphaned file {saved_filename}: {file_e}", exc_info=True)
            return jsonify({'error': 'データベース処理中にエラーが発生しました。'}), 500

        except Exception as e:
            if db:
                db.rollback() # その他の予期せぬエラーでもロールバック
            current_app.logger.error(f"An unexpected error occurred during item creation: {e}", exc_info=True)
            # その他の予期せぬエラーの場合も、保存したファイルを削除
            if saved_filename:
                file_path_to_remove = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], saved_filename)
                try:
                    if os.path.exists(file_path_to_remove):
                        os.remove(file_path_to_remove)
                        current_app.logger.info(f"Successfully removed orphaned file due to unexpected error: {saved_filename}")
                except Exception as file_e:
                    current_app.logger.error(f"Error deleting orphaned file {saved_filename}: {file_e}", exc_info=True)
            return jsonify({'error': 'アイテム作成中に予期せぬエラーが発生しました。'}), 500



    # アイテムを更新するエンドポイント (PATCH)
    @app.route('/api/admin/item/<int:item_id>/edit', methods=['PATCH'])
    def update_item(item_id: int):
        db = get_db()
        new_image_filename = None

        try:
            item = db.query(Item).filter(Item.id == item_id).first()
            if not item:
                return jsonify({"error": "Item not found"}), 404

            # テキストフィールド更新
            if request.form:
                validated = ItemUpdate(**request.form.to_dict())
                for key, value in validated.model_dump(exclude_unset=True).items():
                    setattr(item, key, value)

            # 画像更新
            old_image_filename = getattr(item, 'image_filename', None)
            file = request.files.get('image')
            if file and file.filename:
                new_image_filename = photos.save(file)
                item.image_filename = new_image_filename
                item.image_url = photos.url(new_image_filename)

            # DB更新
            db.commit()

            # 成功時：古いファイルを削除
            if old_image_filename and old_image_filename != new_image_filename and new_image_filename != None:
                _remove_file_safe(old_image_filename)

            return jsonify(item.to_dict()), 200

        except ValidationError as e:
            db.rollback()
            # エラー時：新しいファイルを削除
            if new_image_filename:
                _remove_file_safe(new_image_filename)
            return jsonify({'error': e.errors()}), 400

        except Exception as e:
            db.rollback()
            # エラー時：新しいファイルを削除
            if new_image_filename:
                _remove_file_safe(new_image_filename)
            current_app.logger.error(f"Error: {e}", exc_info=True)
            return jsonify({'error': 'エラーが発生しました。'}), 500


    def _remove_file_safe(filename):
        """ファイルを安全に削除（エラーでも継続）"""
        if not filename:
            return

        file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"Removed image file: {filename}")
        except Exception as e:
            current_app.logger.warning(f"Could not remove file {filename}: {e}")



    # アイテムを削除するエンドポイント (DELETE)
    @app.route('/api/admin/item/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id: int):
        db = get_db()
        try:
            item = db.query(Item).filter(Item.id == item_id).first()
            if item is None:
                return jsonify({"error": "Item not found"}), 404
            db.delete(item)
            db.commit()

            if item.image_filename:
                current_app.logger.warning(item.image_filename)
                _remove_file_safe(item.image_filename)

            return jsonify({"message": "Item deleted successfully"}), 200
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 500






    @app.route('/api/message', methods=['POST'])
    def save_message():
        json_data = request.get_json()

        if not json_data:
            return jsonify({"error": "Request body must be JSON and not empty."}), 400

        try:
            # Pydanticモデルでデータのバリデーションと型変換を行う
            validated_data = MessageCreateSchema(**json_data)
        except ValidationError as e:
            # バリデーションエラーが発生した場合、詳細なエラー情報を返す
            # e.errors() はエラーのリストを返します
            return jsonify({"error": "Validation Failed", "details": e.errors()}), 422 # 422 Unprocessable Entity

        # get_db() が失敗する可能性を考慮し、except ブロック内で db.rollback() を安全に呼び出すために依然として有用な防御的プログラミング
        db = None # finallyブロックで確実にcloseするために、先に定義

        try:
            db = get_db()

            # idはdbによってデータベースによって自動採番される。また、created_atも自動的に入れられる。
            new_message = Message(
                username=validated_data.username,
                email=validated_data.email,
                message=validated_data.message,
            )

            db.add(new_message)
            db.commit()

            # idやcreated_atなどDB側で生成される値を取得するためにリフレッシュ
            db.refresh(new_message)

            result = new_message.to_dict()
            return jsonify(result), 201

        except SQLAlchemyError as e: # DB関連の具体的なエラー
            if db: # dbが取得できていればロールバック
                db.rollback()
            current_app.logger.error(f"Database error saving message: {e}", exc_info=True)
            # ユーザーには具体的なDBエラー詳細を見せない方が良い場合もある
            return jsonify({'error': 'A database error occurred.'}), 500

        except Exception as e: # その他の予期せぬエラー
            # 予期せぬエラーの場合、ロールバックが必要かどうかの判断は難しいが、
            # セッションが不安定な可能性を考慮してロールバックしておくのは安全策
            if db: # dbが取得できていればロールバック
                db.rollback()
            current_app.logger.error(f"Unexpected error saving message: {e}", exc_info=True)
            return jsonify({'error': 'An unexpected error occurred.'}), 500



    # Vue Routerのhistory modeに対応（すべてのルートでindex.htmlを返す）
    @app.route('/<path:path>')
    def catch_all(path):
        # APIルートは除外
        if path.startswith('api/'):
            return {'error': 'API endpoint not found'}, 404

        # 静的ファイルが存在する場合はそれを返す
        if os.path.exists(os.path.join('static', path)):
            return send_from_directory('static', path)

        # それ以外はVue.jsのindex.htmlを返す
        return send_from_directory('static', 'index.html')




