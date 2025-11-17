"""Main Celery task for processing uploaded Excel files."""

import os
import logging

from backend.celery_app import celery_app
from backend.core.config import settings
from backend.core.utils import utcnow
from backend.db.session import SessionLocal
from backend.crud.employee_crud import employee_crud
from backend.crud.project_crud import project_crud
from backend.crud.upload_job_crud import upload_job_crud
from backend.schemas.employee import EmployeeCreate
from backend.schemas.project import ProjectCreate
from backend.services.config_loader import ConfigLoader
from backend.services.excel_reader import ExcelReader
from backend.services.data_validator import DataValidator
from backend.services.data_transformer import DataTransformer

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def process_upload_task(self, job_id: str, file_path: str):
    """Main upload processing task."""
    db = SessionLocal()

    try:
        logger.info(f"[Job {job_id}] Starting processing")

        job = upload_job_crud.get(db, id_value=job_id)
        if not job:
            logger.error(f"[Job {job_id}] Job not found in database")
            return

        job = upload_job_crud.update(db, db_obj=job, obj_in={
            "status": "processing",
            "current_step": "reading",
            "started_at": utcnow()
        })
        db.commit()
        db.refresh(job)

        # Load configuration
        logger.info(f"[Job {job_id}] Loading configuration")
        try:
            config = ConfigLoader()
        except Exception as e:
            raise ValueError(f"Failed to load config.csv: {e}")

        # Read Excel file
        full_file_path = settings.UPLOAD_DIR_ABSOLUTE_PATH / file_path
        logger.info(f"[Job {job_id}] Reading Excel file: {full_file_path}")

        try:
            with ExcelReader(str(full_file_path)) as reader:
                reader.validate_required_sheets(["Employees", "Projects"])
                employees_data = reader.read_sheet("Employees")
                projects_data = reader.read_sheet("Projects")

                total_rows = len(employees_data) + len(projects_data)
                logger.info(
                    f"[Job {job_id}] Read {len(employees_data)} employees, "
                    f"{len(projects_data)} projects"
                )
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

        job = upload_job_crud.update(db, db_obj=job, obj_in={
            "total_rows": total_rows,
            "current_step": "validating"
        })
        db.commit()
        db.refresh(job)

        # Validate and Transform Data
        logger.info(f"[Job {job_id}] Validating and transforming data")

        validator = DataValidator()
        transformer = DataTransformer(config)

        processed_employees = []
        processed_projects = []
        error_details = {"errors": []}
        error_count = 0

        # Process employees
        for idx, row in enumerate(employees_data, start=1):
            excel_row = row.get('_excel_row_number', idx + 1)

            is_valid, error_msg = validator.validate_employee(row)
            if not is_valid:
                error_details["errors"].append({
                    "sheet": "Employees",
                    "row": excel_row,
                    "error": error_msg
                })
                error_count += 1
                logger.warning(f"[Job {job_id}] Employee row {excel_row} validation failed: {error_msg}")
                continue

            try:
                transformed = transformer.transform_employee(row)
                processed_employees.append(transformed)
            except Exception as e:
                error_details["errors"].append({
                    "sheet": "Employees",
                    "row": excel_row,
                    "error": f"Transformation error: {str(e)}"
                })
                error_count += 1
                logger.warning(f"[Job {job_id}] Employee row {excel_row} transformation failed: {e}")

        # Process projects
        for idx, row in enumerate(projects_data, start=1):
            excel_row = row.get('_excel_row_number', idx + 1)

            is_valid, error_msg = validator.validate_project(row)
            if not is_valid:
                error_details["errors"].append({
                    "sheet": "Projects",
                    "row": excel_row,
                    "error": error_msg
                })
                error_count += 1
                logger.warning(f"[Job {job_id}] Project row {excel_row} validation failed: {error_msg}")
                continue

            try:
                transformed = transformer.transform_project(row)
                processed_projects.append(transformed)
            except Exception as e:
                error_details["errors"].append({
                    "sheet": "Projects",
                    "row": excel_row,
                    "error": f"Transformation error: {str(e)}"
                })
                error_count += 1
                logger.warning(f"[Job {job_id}] Project row {excel_row} transformation failed: {e}")

        logger.info(
            f"[Job {job_id}] Validation complete. "
            f"Valid: {len(processed_employees)} employees, {len(processed_projects)} projects. "
            f"Errors: {error_count}"
        )

        # Persist to database
        logger.info(f"[Job {job_id}] Persisting data to database")

        job = upload_job_crud.update(db, db_obj=job, obj_in={
            "current_step": "persisting",
            "processed_rows": len(processed_employees) + len(processed_projects),
            "error_rows": error_count
        })
        db.commit()
        db.refresh(job)

        # Save employees with individual error handling and commit
        saved_employees = 0
        for emp_data in processed_employees:
            try:
                employee_create = EmployeeCreate(**emp_data)
                employee, was_created = employee_crud.upsert(db, obj_in=employee_create)
                db.commit()
                saved_employees += 1

                action = "created" if was_created else "updated"
                logger.debug(f"[Job {job_id}] Employee {emp_data.get('employee_id')} {action}")

            except Exception as e:
                db.rollback()
                error_count += 1
                emp_id = emp_data.get('employee_id', 'unknown')
                logger.error(f"[Job {job_id}] Failed to save employee {emp_id}: {e}")
                error_details["errors"].append({
                    "sheet": "Employees",
                    "row": emp_id,
                    "error": f"Database error: {str(e)}"
                })

        # Save projects with individual error handling and commit
        saved_projects = 0
        for proj_data in processed_projects:
            try:
                project_create = ProjectCreate(**proj_data)
                project, was_created = project_crud.upsert(db, obj_in=project_create)
                db.commit()
                saved_projects += 1

                action = "created" if was_created else "updated"
                logger.debug(f"[Job {job_id}] Project {proj_data.get('project_id')} {action}")

            except Exception as e:
                db.rollback()
                error_count += 1
                proj_id = proj_data.get('project_id', 'unknown')
                logger.error(f"[Job {job_id}] Failed to save project {proj_id}: {e}")
                error_details["errors"].append({
                    "sheet": "Projects",
                    "row": proj_id,
                    "error": f"Database error: {str(e)}"
                })

        logger.info(
            f"[Job {job_id}] Persistence complete. "
            f"Saved: {saved_employees} employees, {saved_projects} projects. "
            f"Failed: {error_count - (len(processed_employees) + len(processed_projects) - saved_employees - saved_projects)}"
        )

        # Complete successfully
        logger.info(f"[Job {job_id}] Processing completed successfully")

        db.refresh(job)
        job = upload_job_crud.update(db, db_obj=job, obj_in={
            "status": "completed",
            "current_step": "completed",
            "processed_rows": saved_employees + saved_projects,
            "error_details": error_details if error_count > 0 else None,
            "error_rows": error_count,
            "completed_at": utcnow()
        })
        db.commit()
        db.refresh(job)

        # Clean up file
        try:
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
                logger.info(f"[Job {job_id}] Cleaned up file: {full_file_path}")
        except Exception as e:
            logger.warning(f"[Job {job_id}] Failed to clean up file: {e}")

        logger.info(
            f"[Job {job_id}] Final stats - "
            f"Saved: {saved_employees + saved_projects}, "
            f"Errors: {error_count}"
        )

    except Exception as e:
        logger.error(f"[Job {job_id}] Processing failed: {e}", exc_info=True)

        try:
            db.rollback()
            job = upload_job_crud.get(db, id_value=job_id)
            if job:
                job = upload_job_crud.update(db, db_obj=job, obj_in={
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": utcnow()
                })
                db.commit()
                db.refresh(job)
        except Exception as update_error:
            logger.error(f"[Job {job_id}] Failed to update job status: {update_error}", exc_info=True)

        raise

    finally:
        db.close()
