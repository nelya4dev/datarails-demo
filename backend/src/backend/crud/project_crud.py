"""CRUD operations for Project model."""

from typing import Tuple
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.project import Project
from backend.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """CRUD operations for Project model.

    Inherits all standard operations from CRUDBase:
    - get(db, id_value) - Get project by UUID
    - get_by_attribute(db, attr_name, attr_value) - Get by any attribute (e.g., project_id)
    - get_multi(db, skip, limit) - Get multiple projects with pagination
    - get_multi_with_filter(db, filters, skip, limit) - Get with filters (e.g., by status)
    - count(db) - Count all projects
    - count_with_filter(db, filters) - Count with filters
    - create(db, obj_in) - Create new project
    - update(db, db_obj, obj_in) - Update existing project
    - remove(db, id_value) - Delete project

    Custom methods:
    - upsert(db, obj_in) - Insert or update based on project_id
    """

    def upsert(self, db: Session, *, obj_in: ProjectCreate) -> Tuple[Project, bool]:
        """Insert or update project based on project_id (business key).

        Checks if project with this project_id already exists:
        - If exists → UPDATE with new data
        - If not exists → INSERT new record

        This enables re-uploading the same file without creating duplicates.

        Args:
            db: Database session for the transaction.
            obj_in: Project data to insert or update.

        Returns:
            Tuple of (project_instance, was_created)
            - project_instance: The created or updated Project model
            - was_created: True if newly inserted, False if updated

        Example:
            project, created = crud_project.upsert(db, obj_in=project_data)
            if created:
                print(f"Inserted new project: {project.project_id}")
            else:
                print(f"Updated existing project: {project.project_id}")

        Note:
            Uses get_by_attribute() from base class to check for existing record.
            Uses update() and create() from base class for the actual operations.
        """
        existing = self.get_by_attribute(db, "project_id", obj_in.project_id)

        if existing:
            updated = self.update(db, db_obj=existing, obj_in=obj_in)
            return updated, False
        else:
            created = self.create(db, obj_in=obj_in)
            return created, True


project_crud = CRUDProject(Project)
