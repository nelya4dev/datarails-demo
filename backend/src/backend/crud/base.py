from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations on SQLAlchemy models.

    Provides standard database operations (Create, Read, Update, Delete) for any
    SQLAlchemy model. Uses Pydantic schemas for input validation and serialization.

    Attributes:
        model: The SQLAlchemy model class this CRUD instance operates on.
    """

    def __init__(self, model: Type[ModelType]):
        """Initialize CRUD operations for a specific model.

        Args:
            model: SQLAlchemy model class to perform CRUD operations on.
        """
        self.model = model

    def get(self, db: Session, id_value: Any) -> Optional[ModelType]:
        """Get a single record by primary key ID.

        Args:
            db: Database session for the query.
            id_value: Primary key value to search for (usually UUID or int).

        Returns:
            Model instance if found, None otherwise.
        """
        return db.query(self.model).filter(self.model.id == id_value).first()  # type: ignore

    def get_by_attribute(
            self,
            db: Session,
            attr_name: str,
            attr_value: Any
    ) -> Optional[ModelType]:
        """Get a single record by any model attribute.

        Args:
            db: Database session for the query.
            attr_name: Name of the model attribute to filter by (e.g., "email").
            attr_value: Value to search for in the specified attribute.

        Returns:
            First model instance matching the criteria, None if not found.

        Note:
            Returns only the first match. For multiple results, use a custom
            query or extend this method in your CRUD class.
        """
        return db.query(self.model).filter(getattr(self.model, attr_name) == attr_value).first()  # type: ignore

    def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 5000
    ) -> List[ModelType]:
        """Get multiple records with pagination.

        Args:
            db: Database session for the query.
            skip: Number of records to skip (offset). Defaults to 0.
            limit: Maximum number of records to return. Defaults to 5000.

        Returns:
            List of model instances, ordered by ID ascending.

        Note:
            Results are ordered by model.id by default. Override in subclass
            for custom ordering.
        """
        return (
            db.query(self.model)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_with_filter(
            self,
            db: Session,
            *,
            filters: Optional[Dict[str, Any]] = None,
            skip: int = 0,
            limit: int = 5000
    ) -> List[ModelType]:
        """Get multiple records with optional filters and pagination.

        Applies equality filters to model attributes and returns paginated results.
        If no filters provided, behaves like get_multi().

        Args:
            db: Database session for the query.
            filters: Dictionary of attribute names and values to filter by.
                Example: {"department_name": "HR", "status": "active"}
                Each filter applies an equality check (attr == value).
                If None or empty, no filters are applied.
            skip: Number of records to skip (offset). Defaults to 0.
            limit: Maximum number of records to return. Defaults to 5000.

        Returns:
            List of model instances matching all filters, ordered by ID ascending.

        Note:
            All filters must match (AND logic, not OR).
            Results are ordered by model.id by default.

        Example:
            # Get employees in HR department with pagination
            employees = crud.get_multi_with_filter(
                db,
                filters={"department_name": "Human Resources"},
                skip=0,
                limit=20
            )

            # Get active projects with budget > handled by custom CRUD method
            # This method only supports equality (==) filters
        """
        query = db.query(self.model)

        if filters:
            for attr_name, attr_value in filters.items():
                query = query.filter(getattr(self.model, attr_name) == attr_value)

        return query.order_by(self.model.id).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        """Get total count of all records.

        Args:
            db: Database session for the query.

        Returns:
            Total number of records in the table.
        """
        return db.query(self.model).count()

    def count_with_filter(
            self,
            db: Session,
            *,
            filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Get count of records matching optional filters.

        Applies equality filters to model attributes and returns count.
        If no filters provided, behaves like count().

        Args:
            db: Database session for the query.
            filters: Dictionary of attribute names and values to filter by.
                Example: {"department_name": "HR", "status": "active"}
                Each filter applies an equality check (attr == value).
                If None or empty, no filters are applied.

        Returns:
            Total number of records matching all filters.

        Note:
            All filters must match (AND logic, not OR).
            Used for pagination metadata (calculating total pages).
        """
        query = db.query(self.model)

        if filters:
            for attr_name, attr_value in filters.items():
                query = query.filter(getattr(self.model, attr_name) == attr_value)

        return query.count()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record in the database.

        Args:
            db: Database session for the transaction.
            obj_in: Pydantic schema containing data for the new record.
                All required fields must be present and valid.

        Returns:
            Newly created model instance with database-generated fields
            (like ID, timestamps) populated.

        Note:
            The obj_in schema is converted to a dict using jsonable_encoder
            before creating the model instance. This handles Pydantic models,
            enums, and other complex types correctly.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record with new data.

        Only fields present in obj_in will be updated. Other fields remain unchanged.

        Args:
            db: Database session for the transaction.
            db_obj: Existing model instance to update (must be attached to session).
            obj_in: Pydantic schema or dict with update data.
                Only fields with values will be updated (exclude_unset=True).

        Returns:
            Updated model instance with refreshed data from database.

        Note:
            Partial updates are supported - only provide fields you want to change.
            The exclude_unset=True parameter ensures unset fields are not updated
            to None.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            if hasattr(obj_in, "model_dump"):
                update_data = obj_in.model_dump(exclude_unset=True)
            else:
                update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id_value: int) -> ModelType:
        """Remove a record permanently from the database.

        Args:
            db: Database session for the transaction.
            id_value: Primary key ID of the record to delete.

        Returns:
            The deleted model instance, or None if not found.
        """
        obj = db.query(self.model).get(id_value)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
