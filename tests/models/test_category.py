from sqlalchemy import Boolean, Integer, String

"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("categories")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_type(db_inspector):
    table = "categories"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_column_nullable(db_inspector):
    table = "categories"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["id"]["nullable"] is False
    assert columns["name"]["nullable"] is False
    assert columns["slug"]["nullable"] is False
    assert columns["is_active"]["nullable"] is False
    assert columns["level"]["nullable"] is False
    assert columns["parent_id"]["nullable"] is True


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


def test_model_structure_column_constraints(db_inspector):
    table = "categories"
    constants = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "name_length_check" for constraint in constants)
    assert any(constraint["name"] == "slug_length_check" for constraint in constants)


"""
- [ ] Verify the correctness of default values for relevant columns.
"""


def test_model_structure_column_default_values(db_inspector):
    table = "categories"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["is_active"]["default"] == "false"
    assert columns["level"]["default"] == "100"


"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_length(db_inspector):
    table = "categories"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
    assert columns["slug"]["type"].length == 120


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_column_unique(db_inspector):
    table = "categories"
    constants = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_categories_name_level" for constraint in constants
    )
    assert any(constraint["name"] == "uq_categories_slug" for constraint in constants)
