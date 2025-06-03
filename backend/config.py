from flask_uploads import UploadSet, configure_uploads, IMAGES
from pathlib import Path

# 'photos'：この名前(UploadSetの第一引数)がUPLOADED_PHOTOS_DESTのPHOTOS部分(大文字)と対応
# IMAGES：jpg, jpeg, png, gif などの画像ファイルのみ許可
photos = UploadSet('photos', IMAGES)

def configure_app(app):


    # 保存先
    app.config['UPLOADED_PHOTOS_DEST'] = str(Path.cwd() / 'frontend' / 'src' / 'assets' / 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # ファイルサイズ上限

    # 以下の設定は開発用であり、本番環境では、UPLOADS_DEFAULT_URL を設定し、Web サーバーを使用してファイルを提供することを推奨します。
    app.config['UPLOADS_AUTOSERVE'] = True

    # UploadSetをアプリに登録
    configure_uploads(app, photos)

