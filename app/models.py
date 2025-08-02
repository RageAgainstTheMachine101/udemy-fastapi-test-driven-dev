from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from .db_connection import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default=100, server_default="100")
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="category_name_length_check"),
        CheckConstraint("length(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint("slug", name="uq_categories_slug"),
        UniqueConstraint("name", "level", name="uq_categories_name_level"),
    )


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    pid = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        server_default=text("uuid_generate_v4()"),
    )
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="False")
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
    )
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    stock_status = Column(
        Enum("InStock", "OutOfStock", "OnBackorder", name="status_enum"),
        nullable=False,
        default="OutOfStock",
        server_default="OutOfStock",
    )
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    # seasonal_id = Column(String(100), ForeignKey("seasonal_events.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="product_name_length_check"),
        CheckConstraint("length(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("slug", name="uq_product_slug"),
        UniqueConstraint("name", name="uq_product_name"),
    )
