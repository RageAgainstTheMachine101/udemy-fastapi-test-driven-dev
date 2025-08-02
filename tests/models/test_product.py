from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("products")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_type(db_inspector):
    table = "products"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["pid"]["type"], UUID)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["is_digital"]["type"], Boolean)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    assert isinstance(columns["stock_status"]["type"], Enum)
    assert isinstance(columns["category_id"]["type"], Integer)
    # assert isinstance(columns["seasonal_events"]["type"], String)


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_column_nullable(db_inspector):
    table = "products"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["id"]["nullable"] is False
    assert columns["pid"]["nullable"] is False
    assert columns["name"]["nullable"] is False
    assert columns["slug"]["nullable"] is False
    assert columns["description"]["nullable"] is True
    assert columns["is_digital"]["nullable"] is False
    assert columns["created_at"]["nullable"] is False
    assert columns["updated_at"]["nullable"] is False
    assert columns["is_active"]["nullable"] is False
    assert columns["stock_status"]["nullable"] is False
    assert columns["category_id"]["nullable"] is False
    # assert columns["seasonal_events"]["nullable"] is True


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


def test_model_structure_column_constraints(db_inspector):
    table = "products"
    constants = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "product_name_length_check" for constraint in constants
    )
    assert any(
        constraint["name"] == "product_slug_length_check" for constraint in constants
    )


"""
- [ ] Verify the correctness of default values for relevant columns.
"""


def test_model_structure_column_default_values(db_inspector):
    table = "products"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["is_digital"]["default"] == "false"
    assert columns["is_active"]["default"] == "false"
    assert columns["stock_status"]["default"] == "'OutOfStock'::status_enum"


"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_length(db_inspector):
    table = "products"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 200
    assert columns["slug"]["type"].length == 220


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_column_unique(db_inspector):
    table = "products"
    constants = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_product_name" for constraint in constants)
    assert any(constraint["name"] == "uq_product_slug" for constraint in constants)
