"""Data transformer for applying config-based transformations."""

from datetime import date, datetime
from typing import Dict, Optional, Any
from backend.services.config_loader import ConfigLoader


class DataTransformer:
    """Transform raw Excel data using config.csv rules.

    Applies transformations like:
    - Department code → Department name mapping
    - Currency conversion (salary → annual_salary_eur)
    - Date calculations (hire_date → tenure_years)
    """

    def __init__(self, config: ConfigLoader):
        """Initialize transformer with config.

        Args:
            config: ConfigLoader instance with transformation rules
        """
        self.config = config

    def transform_employee(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Transform employee row with config-based rules.

        Args:
            row: Raw employee data from Excel

        Returns:
            Dictionary with both original and transformed fields

        Example:
            Input:  {'employee_id': 'E0001', 'department_code': 'HR', 'salary': 78289, ...}
            Output: {
                'employee_id': 'E0001',
                'name': 'Kevin Davis',
                'department_code': 'HR',
                'salary': 78289,
                'hire_date': date(2023, 4, 5),
                'department_name': 'Human Resources',  # ← Transformed
                'annual_salary_eur': 72025.88,         # ← Transformed
                'tenure_years': 2                       # ← Calculated
            }
        """
        # Start with original data
        transformed = row.copy()

        # Remove Excel row number (internal use only)
        transformed.pop('_excel_row_number', None)

        # Transform department_code → department_name
        dept_code = row.get('department_code')
        if dept_code:
            dept_name = self.config.get_department_name(dept_code)
            transformed['department_name'] = dept_name
        else:
            transformed['department_name'] = None

        # Transform salary → annual_salary_eur
        salary = row.get('salary')
        if salary is not None:
            try:
                salary_float = float(salary)
                exchange_rate = self.config.get_exchange_rate()
                transformed['annual_salary_eur'] = round(salary_float * exchange_rate, 2)
            except (ValueError, TypeError):
                transformed['annual_salary_eur'] = None
        else:
            transformed['annual_salary_eur'] = None

        # Calculate hire_date → tenure_years
        hire_date = row.get('hire_date')
        if hire_date:
            transformed['tenure_years'] = self.calculate_tenure(hire_date)
        else:
            transformed['tenure_years'] = None

        return transformed

    def transform_project(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Transform project row.

        Currently projects don't have transformations in config.csv,
        but this method provides structure for future additions.

        Args:
            row: Raw project data from Excel

        Returns:
            Dictionary with project data (cleaned)
        """
        # Start with original data
        transformed = row.copy()

        # Remove Excel row number
        transformed.pop('_excel_row_number', None)

        # Ensure budget_usd is float
        budget = row.get('budget_usd')
        if budget is not None:
            try:
                transformed['budget_usd'] = float(budget)
            except (ValueError, TypeError):
                transformed['budget_usd'] = None

        return transformed

    @staticmethod
    def calculate_tenure(hire_date: Optional[date]) -> Optional[int]:
        """Calculate years of service from hire date.

        Args:
            hire_date: Employee hire date

        Returns:
            Number of years employed (integer) or None
        """
        if not hire_date:
            return None

        if not isinstance(hire_date, date):
            return None

        today = date.today()
        years = (today - hire_date).days // 365
        return years

    @staticmethod
    def parse_date(date_value: Any) -> Optional[date]:
        """Parse various date formats to date object.

        Args:
            date_value: Date in various formats (date, datetime, string)

        Returns:
            date object or None
        """
        if date_value is None:
            return None

        # Already a date
        if isinstance(date_value, date):
            return date_value

        # datetime → date
        if isinstance(date_value, datetime):
            return date_value.date()

        # String parsing (DD/MM/YYYY format from Excel)
        if isinstance(date_value, str):
            try:
                # Try DD/MM/YYYY format
                return datetime.strptime(date_value.strip(), "%d/%m/%Y").date()
            except ValueError:
                try:
                    # Try YYYY-MM-DD format
                    return datetime.strptime(date_value.strip(), "%Y-%m-%d").date()
                except ValueError:
                    return None

        return None
