from flask import json
from flask_login import UserMixin
from hivemind.core.extensions import db
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String, Text
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(50), default='static/images/default.jpg')
    password_hash: Mapped[str] = mapped_column(String(128)) 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "profile_picture": self.profile_picture
        }
    
    

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

class ChatroomParticipant(db.Model):
    chatroom_id: Mapped[int] = mapped_column(ForeignKey("chatroom.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    __table_args__ = (
        PrimaryKeyConstraint("chatroom_id", "user_id"),
    )