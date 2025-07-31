from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Integer,
    String,
    UniqueConstraint,
)

from .db_connection import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default=100, server_default="100")
    parent_id = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="name_length_check"),
        CheckConstraint("length(slug) > 0", name="slug_length_check"),
        UniqueConstraint("slug", name="uq_categories_slug"),
        UniqueConstraint("name", "level", name="uq_categories_name_level"),
    )
