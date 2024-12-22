from flask import url_for
from hivemind.core.extensions import db
from sqlalchemy import ForeignKey, String, Text
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(50), default='static/images/default.jpg')

class ChatMessage(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    chatroom_id: Mapped[int] = mapped_column(ForeignKey("chatroom.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default= lambda: datetime.now(timezone.utc), index=True)

    def time_since_creation(self) -> timedelta:
        timestamp = self.timestamp.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        td = now - timestamp
        return td

class Chatroom(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default= lambda: datetime.now(timezone.utc), index=True)