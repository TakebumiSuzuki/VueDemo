from datetime import datetime # datetime型を型ヒントで使用
from sqlalchemy import String, DateTime, Integer, CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column
# func オブジェクトは、SQLAlchemyがデータベースサーバー側で実行されるSQL関数を表現するためのものです。
# SQLAlchemyがデータベースの方言 (dialect) に応じて適切なSQL関数に変換してくれる抽象的な表現
from sqlalchemy.sql import func
from .database import Base
from pydantic import BaseModel, EmailStr, constr, Field, ValidationError


# str | None は Python 3.10以降で導入された標準の型ヒント構文で、
# 3.9以前でのtyping.Optional[str] や typing.Union[str, None] と同じ意味を持ちます。
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    price: Mapped[int] = mapped_column(Integer, CheckConstraint('price > 0', name='positive_price'), index=True)
    # 画像URL保存用フィールド フロントエンドで表示するためのフルURL
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # 画像のファイル名も保存（削除時などに便利）サーバー上のファイル管理用
    image_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, category={self.category}, price={self.price})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ItemCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=1000)
    category: str = Field(..., max_length=50)
    price: int = Field(..., gt=0)
    # image_url と image_filename はファイルアップロード後に設定するため、
    # リクエストボディからは提供されないことを想定し Optional で良い。
    image_url: str | None = Field(None, max_length=500)
    image_filename: str | None = Field(None, max_length=255)
    # id, created_at, updated_at はDB側で自動生成されるため、入力には含めない


class ItemUpdate(BaseModel):
    name: str | None = Field(..., max_length=100)
    description: str | None = Field(None, max_length=1000)
    category: str | None = Field(..., max_length=50)
    price: int | None = Field(..., gt=0)
    # image_url と image_filename はファイルアップロード後に設定するため、
    # リクエストボディからは提供されないことを想定し Optional で良い。
    image_url: str | None = Field(None, max_length=500)
    image_filename: str | None = Field(None, max_length=255)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(100), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()
)

    def __repr__(self):
        message_preview = ""
        if self.message:
            message_preview = self.message[:30] + "..." if len(self.message) > 30 else self.message

        return (f"<Message(id={self.id}, username='{self.username}', "
                f"email='{self.email}', message='{message_preview}')>")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class MessageCreateSchema(BaseModel):
    # ...は、そのフィールドが必須であることを示します。
    username: str = Field(..., min_length=1, max_length=50, description="ユーザー名")
    email: EmailStr = Field(..., description="メールアドレス") # EmailStrがメール形式を検証
    message: str = Field(..., min_length=1, description="メッセージ本文")