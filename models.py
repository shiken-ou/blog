from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from config import DevelopmentConfig

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    username: Mapped[str] = mapped_column(String(10), unique= True, nullable= False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable= False)

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    title: Mapped[str] = mapped_column(String(30), nullable= False)
    content: Mapped[str] = mapped_column(Text, nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), default= lambda :datetime.now(timezone.utc))