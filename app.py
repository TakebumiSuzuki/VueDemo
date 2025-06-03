from backend import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app() # ファクトリ関数を呼び出してアプリケーションインスタンスを取得

if __name__ == '__main__':
    # app.run(debug=True)
    debug_mode = os.environ.get('FLASK_ENV') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
