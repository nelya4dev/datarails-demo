"""CRUD operations for UploadJob model."""

from typing import List, Optional
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.upload_job import UploadJob
from backend.schemas.upload_job import UploadJobCreate, UploadJobUpdate


class CRUDUploadJob(CRUDBase[UploadJob, UploadJobCreate, UploadJobUpdate]):
    """CRUD operations for UploadJob model.

    Inherits all standard operations from CRUDBase:
    - get(db, id_value) - Get job by UUID
    - get_by_attribute(db, attr_name, attr_value) - Get by any attribute
    - get_multi(db, skip, limit) - Get multiple jobs with pagination
    - get_multi_with_filter(db, filters, skip, limit) - Get with filters (e.g., by status)
    - count(db) - Count all jobs
    - count_with_filter(db, filters) - Count with filters
    - create(db, obj_in) - Create new job
    - update(db, db_obj, obj_in) - Update existing job
    - remove(db, id_value) - Delete job

    Custom methods:
    - get_jobs_ordered(db, filters, skip, limit) - Get jobs with custom ordering (created_at DESC)

    Note: UploadJob doesn't need upsert() because each upload creates a unique job.
    """

    def get_jobs_ordered(
            self,
            db: Session,
            *,
            filters: Optional[dict] = None,
            skip: int = 0,
            limit: int = 20
    ) -> List[UploadJob]:
        """Get upload jobs with custom ordering (newest first).

        Similar to get_multi_with_filter() but with DESC ordering by created_at
        instead of ASC ordering by id. This is the primary way to retrieve jobs
        for the jobs list endpoint.

        Args:
            db: Database session for the query.
            filters: Optional dictionary of filters.
                Example: {"status": "pending"} or {"status": "completed"}
                If None or empty, returns all jobs.
            skip: Number of records to skip (offset). Defaults to 0.
            limit: Maximum number of records to return. Defaults to 20.

        Returns:
            List of UploadJob instances ordered by created_at DESC (newest first).

        Example:
            # Get all jobs (newest first)
            jobs = crud_upload_job.get_jobs_ordered(db, skip=0, limit=20)

            # Get pending jobs only
            pending_jobs = crud_upload_job.get_jobs_ordered(
                db,
                filters={"status": "pending"},
                skip=0,
                limit=20
            )

            # Get completed jobs, page 2
            completed_jobs = crud_upload_job.get_jobs_ordered(
                db,
                filters={"status": "completed"},
                skip=20,
                limit=20
            )

        Note:
            This is the ONLY custom method needed for UploadJob.
            For simple queries by status, you can also use base methods:
            - get_by_attribute(db, "status", "pending") - Get first pending job
            - get_multi_with_filter(db, filters={"status": "pending"}) - Get all (ordered by id)

            But for job listings, we want newest-first ordering, so this method exists.
        """
        query = db.query(self.model)

        if filters:
            for attr_name, attr_value in filters.items():
                query = query.filter(getattr(self.model, attr_name) == attr_value)

        return (
            query
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


upload_job_crud = CRUDUploadJob(UploadJob)
