import typing as t
import re
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """SQLAlchemy declarative base with automatic table name generation.

    Base class for all ORM models providing:
    - Automatic table naming from class name (CamelCase → snake_case)
    - Common id attribute declaration
    - SQLAlchemy 2.0 declarative style

    Table Naming Examples:
        - ApiRequest → api_request
        - Employee → employee

    All model classes should inherit from this Base class. The __tablename__
    is automatically generated unless explicitly overridden.

    Attributes:
        id: Declared as t.Any to allow subclasses to define their own type
            (UUID, int, str, etc.). Must be redeclared in each model with
            specific type.
    """
    id: t.Any

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name using snake_case convention."""
        name = re.sub('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', cls.__name__)
        return name.lower()
