from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    role = Column(Enum('editor', 'admin', name='user_role'), default='editor', nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    created_content = relationship("Content", back_populates="creator", foreign_keys="[Content.created_by]")
    created_magazines = relationship("Magazine", back_populates="creator", foreign_keys="[Magazine.created_by]")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>" 