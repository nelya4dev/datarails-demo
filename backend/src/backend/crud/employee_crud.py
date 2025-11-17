"""CRUD operations for Employee model."""

from typing import Tuple
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.employee import Employee
from backend.schemas.employee import EmployeeCreate, EmployeeUpdate


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    """CRUD operations for Employee model.

    Inherits all standard operations from CRUDBase:
    - get(db, id_value) - Get employee by UUID
    - get_by_attribute(db, attr_name, attr_value) - Get by any attribute (e.g., employee_id)
    - get_multi(db, skip, limit) - Get multiple employees with pagination
    - get_multi_with_filter(db, filters, skip, limit) - Get with filters (e.g., by department)
    - count(db) - Count all employees
    - count_with_filter(db, filters) - Count with filters
    - create(db, obj_in) - Create new employee
    - update(db, db_obj, obj_in) - Update existing employee
    - remove(db, id_value) - Delete employee

    Custom methods:
    - upsert(db, obj_in) - Insert or update based on employee_id
    """

    def upsert(self, db: Session, *, obj_in: EmployeeCreate) -> Tuple[Employee, bool]:
        """Insert or update employee based on employee_id (business key).

        Checks if employee with this employee_id already exists:
        - If exists → UPDATE with new data
        - If not exists → INSERT new record

        This enables re-uploading the same file without creating duplicates.

        Args:
            db: Database session for the transaction.
            obj_in: Employee data to insert or update.

        Returns:
            Tuple of (employee_instance, was_created)
            - employee_instance: The created or updated Employee model
            - was_created: True if newly inserted, False if updated

        Note:
            Uses get_by_attribute() from base class to check for existing record.
            Uses update() and create() from base class for the actual operations.
        """
        existing = self.get_by_attribute(db, "employee_id", obj_in.employee_id)

        if existing:
            updated = self.update(db, db_obj=existing, obj_in=obj_in)
            return updated, False
        else:
            created = self.create(db, obj_in=obj_in)
            return created, True


employee_crud = CRUDEmployee(Employee)
