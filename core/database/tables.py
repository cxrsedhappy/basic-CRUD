from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampsMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow(), onupdate=datetime.now)


class User(Base, TimestampsMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: list[Post] = relationship('Post', backref='user')

    def __init__(self, username, password, **kwargs):
        self.username = kwargs.get('username', username)
        self.password = kwargs.get('password', password)

    def __repr__(self):
        return f'<User id={self.id} name={self.username} email={self.email}>'


class Post(Base, TimestampsMixin):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    text: Mapped[TEXT] = mapped_column(TEXT(collation='utf8'), nullable=False)  # Never tries to support emojis

    def __init__(self, user_id, text, **kwargs):
        self.user_id = kwargs.get('user_id', user_id)
        self.text = kwargs.get('text', text)

    def __repr__(self):
        return f'<Post id={self.id} author_id={self.user_id} text={self.email[:10]}>'
