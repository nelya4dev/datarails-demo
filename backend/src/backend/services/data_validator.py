"""Data validator for validating Excel row data."""

from typing import Tuple, Optional, Dict, Any
from datetime import date


class DataValidator:
    """Validate employee and project data from Excel.

    Validates required fields, data types, and business rules.
    Returns (is_valid, error_message) tuples for easy error handling.
    """

    @staticmethod
    def validate_employee(row: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate employee row data.

        Args:
            row: Dictionary containing employee data from Excel

        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if valid
            - (False, "error message") if invalid

        Validates:
            - employee_id is present and non-empty
            - salary is present and numeric
            - hire_date is a date object (if present)
        """
        # Check employee_id exists
        employee_id = row.get("employee_id")
        if not employee_id:
            return False, "employee_id is required"

        # Check employee_id is not just whitespace
        if isinstance(employee_id, str) and not employee_id.strip():
            return False, "employee_id cannot be empty"

        # Validate salary is required and numeric
        salary = row.get("salary")
        if salary is None or salary == '':
            return False, "salary is required"

        if not isinstance(salary, (int, float)):
            try:
                float(salary)
            except (ValueError, TypeError):
                return False, f"salary must be numeric, got: {salary}"

        # Validate hire_date (if present)
        hire_date = row.get("hire_date")
        if hire_date is not None:
            if not isinstance(hire_date, date):
                return False, f"hire_date must be a date, got: {type(hire_date).__name__}"

        return True, None

    @staticmethod
    def validate_project(row: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate project row data.

        Args:
            row: Dictionary containing project data from Excel

        Returns:
            Tuple of (is_valid, error_message)

        Validates:
            - project_id is present and non-empty
            - budget_usd is numeric (if present)
            - start_date is a date object (if present)
        """
        # Check project_id exists
        project_id = row.get("project_id")
        if not project_id:
            return False, "project_id is required"

        # Check project_id is not just whitespace
        if isinstance(project_id, str) and not project_id.strip():
            return False, "project_id cannot be empty"

        # Validate budget_usd (if present)
        budget_usd = row.get("budget_usd")
        if budget_usd is not None:
            if not isinstance(budget_usd, (int, float)):
                try:
                    float(budget_usd)
                except (ValueError, TypeError):
                    return False, f"budget_usd must be numeric, got: {budget_usd}"

        # Validate start_date (if present)
        start_date = row.get("start_date")
        if start_date is not None:
            if not isinstance(start_date, date):
                return False, f"start_date must be a date, got: {type(start_date).__name__}"

        return True, None

    @staticmethod
    def validate_required_fields(
            row: Dict[str, Any],
            required_fields: list[str]
    ) -> Tuple[bool, Optional[str]]:
        """Generic validation for required fields.

        Args:
            row: Data row dictionary
            required_fields: List of required field names

        Returns:
            Tuple of (is_valid, error_message)
        """
        missing_fields = []

        for field in required_fields:
            value = row.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        return True, None
