from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)

    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title[:20]}')>"
