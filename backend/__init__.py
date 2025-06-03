# g はアプリケーションコンテキストに紐づいた、辞書のように使えるオブジェクトで、HTTPリクエストごとに、
# そのリクエスト専用の g が用意される。リクエスト処理中は、その g を通じて情報を共有できる。
# リクエスト処理が終了すると、g も破棄される。
from flask import Flask, g
from .database import SessionLocal, init_db as original_init_db # init_dbをリネームして衝突を避ける
from .routes import register_routes
from backend.config import configure_app



def create_app(config_object=None): # 設定オブジェクトを受け取れるようにするとより柔軟
    # Flaskは、__name__ から得られるモジュール名を手がかりに、そのモジュールがファイルシステム上のどこに存在するか
    # つまり、そのモジュールのパスを特定しようとします
    # ルートパスを基準に、templates フォルダや static フォルダを探します。
    app = Flask(
        __name__.split('.')[0],
        static_url_path='/'  
    )

    configure_app(app) # 自前で作ったconfigure関数(config.pyも自前で作った)

    # 設定をロードする場合（例）
    # if config_object:
    #     app.config.from_object(config_object)
    # else:
    #     app.config.from_mapping(
    #         SECRET_KEY='dev', # 例: 開発用のシークレットキー
    #         # 他のデフォルト設定
    #     )

    def get_db():
        """リクエストスコープでのデータベースセッション取得"""
        if 'db_session' not in g:
            g.db_session = SessionLocal()
        return g.db_session

    def close_db(error):
        """リクエスト終了時のセッションクリーンアップ"""
        db_session = g.pop('db_session', None)
        if db_session is not None: # ここでNoneチェックを追加！
            db_session.close()
        # db_session.close()

    # アプリケーションコンテキストが終了する際にDBセッションをクローズする
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db(exception)

    # DB初期化コマンドをFlask CLIに追加
    @app.cli.command('init-db')
    def init_db_command():
        # データベース内に対応するテーブルが存在しない場合にのみテーブルを作成します。
        # 既にテーブルが存在する場合は、そのテーブルやデータには何も変更を加えません
        original_init_db() # database.pyのinit_dbを呼び出す
        print("Initialized the database.") # ユーザーへのフィードバック


    register_routes(app, get_db)

    return app