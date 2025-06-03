from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# データベースファイルのパス (SQLiteの場合)
# プロジェクトルートからの相対パスで backend/your_database.db となるように設定
DATABASE_URL = "sqlite:///./backend/test.db"
# DATABASE_URL = "postgresql://user:password@host:port/database"
# DATABASE_URL = "mysql+mysqlclient://user:password@host:port/database"

# データベースエンジンを作成
# connect_args は SQLite の場合にのみ推奨されます（スレッドセーフティのため）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False # 開発時はTrueに設定してSQLログを確認
)

# セッションファクトリを作成
# autocommit=False, autoflush=False に設定し、トランザクション制御を明示的に行う
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# モデルクラスが継承するためのベースクラスで、このクラスには、自身を継承したサブクラスが定義されたときに、そのサブクラスの情報を自動的に収集し、
# メタデータ（MetaDataオブジェクト、この場合は Base.metadata）にテーブル定義として登録する機能が備わっています。
class Base(DeclarativeBase):
    pass


def init_db():
    try:
        # ここでimportされるすべてのモデル（Baseを継承しているもの）がデータベースにテーブルとして作成されます。
        # つまり models.py 内のクラスが Base.metadata に登録される
        import backend.models
        Base.metadata.create_all(bind=engine)
        print("Initialized the database.")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise