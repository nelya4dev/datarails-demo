"""Configuration loader for parsing and accessing config.csv transformations."""

import csv
from typing import Dict, Optional, Any
from backend.core.config import settings


class ConfigLoader:
    """Parse and provide access to config.csv transformation rules.

    Handles the actual config.csv format:
        source_sheet,source_field,target_field,transformation_type,parameters
        Employees,department_code,department_name,MAPPING,"HR:Human Resources, DEV:Development"
        Employees,salary,annual_salary_eur,CALCULATION,0.92
    """

    def __init__(self):
        """Initialize the config loader.

        Uses settings.CONFIG_CSV_ABSOLUTE_PATH to locate config file.

        Raises:
            FileNotFoundError: If config.csv doesn't exist
            ValueError: If CONFIG_CSV_PATH not set in environment
        """
        if not settings.CONFIG_CSV_PATH:
            raise ValueError(
                "CONFIG_CSV_PATH not set in environment. "
                "Please set CONFIG_CSV_PATH in .env file."
            )

        self.config_path = settings.CONFIG_CSV_ABSOLUTE_PATH
        self.mappings: Dict[str, Dict[str, str]] = {}
        self.calculations: Dict[str, Any] = {}
        self.transformations: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self):
        """Load config.csv and parse transformations."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                source_sheet = row['source_sheet'].strip()
                source_field = row['source_field'].strip()
                target_field = row['target_field'].strip()
                transformation_type = row['transformation_type'].strip()
                parameters = row['parameters'].strip()

                # Store in structured format
                key = f"{source_sheet}.{source_field}"

                self.transformations[key] = {
                    'target_field': target_field,
                    'type': transformation_type,
                    'parameters': parameters
                }

                # Parse specific transformation types
                if transformation_type == 'MAPPING':
                    self._parse_mapping(source_field, parameters)
                elif transformation_type == 'CALCULATION':
                    self._parse_calculation(source_field, target_field, parameters)

    def _parse_mapping(self, source_field: str, parameters: str):
        """Parse mapping parameters.

        Example: "HR:Human Resources, DEV:Development, FIN:Finance"
        """
        if source_field not in self.mappings:
            self.mappings[source_field] = {}

        # Parse comma-separated key:value pairs
        pairs = parameters.split(',')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                self.mappings[source_field][key.strip()] = value.strip()

    def _parse_calculation(self, source_field: str, target_field: str, parameters: str):
        """Parse calculation parameters.

        Examples:
            0.92 → multiplication factor
            DATE_DIFF_TO_NOW → date calculation type
        """
        self.calculations[f"{source_field}->{target_field}"] = parameters

    def get_department_name(self, code: Optional[str]) -> Optional[str]:
        """Get department name from code.

        Args:
            code: Department code (e.g., "HR", "DEV")

        Returns:
            Department name or None
        """
        if not code:
            return None
        return self.mappings.get("department_code", {}).get(code.strip())

    def get_exchange_rate(self, source_field: str = "salary",
                          target_field: str = "annual_salary_eur") -> float:
        """Get exchange rate for salary conversion.

        Args:
            source_field: Source field name (default: "salary")
            target_field: Target field name (default: "annual_salary_eur")

        Returns:
            Exchange rate as float, defaults to 1.0
        """
        key = f"{source_field}->{target_field}"
        calc = self.calculations.get(key)

        if calc:
            try:
                return float(calc)
            except ValueError:
                pass

        return 1.0

    def get_transformation(self, sheet: str, field: str) -> Optional[Dict[str, Any]]:
        """Get transformation config for a field.

        Args:
            sheet: Sheet name (e.g., "Employees", "Projects")
            field: Field name (e.g., "department_code")

        Returns:
            Transformation config dict or None
        """
        key = f"{sheet}.{field}"
        return self.transformations.get(key)

    def requires_date_calculation(self, source_field: str, target_field: str) -> bool:
        """Check if field requires date calculation.

        Args:
            source_field: Source field (e.g., "hire_date")
            target_field: Target field (e.g., "tenure_years")

        Returns:
            True if DATE_DIFF_TO_NOW calculation needed
        """
        key = f"{source_field}->{target_field}"
        calc = self.calculations.get(key)
        return calc == "DATE_DIFF_TO_NOW"

    def get_all_mappings(self, field: str) -> Dict[str, str]:
        """Get all mappings for a field.

        Args:
            field: Field name (e.g., "department_code")

        Returns:
            Dictionary of mappings
        """
        return self.mappings.get(field, {}).copy()

    def __repr__(self) -> str:
        return (
            f"<ConfigLoader "
            f"mappings={len(self.mappings)} "
            f"calculations={len(self.calculations)} "
            f"transformations={len(self.transformations)}>"
        )


# Singleton instance
_config_loader_instance: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Get or create singleton ConfigLoader instance."""
    global _config_loader_instance

    if _config_loader_instance is None:
        _config_loader_instance = ConfigLoader()

    return _config_loader_instance


def reload_config() -> ConfigLoader:
    """Reload config from file."""
    global _config_loader_instance
    _config_loader_instance = ConfigLoader()
    return _config_loader_instance
