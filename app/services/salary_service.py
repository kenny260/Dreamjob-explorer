"""
salary_service.py
Provides expected salary data for multiple regions (Africa + Western).
"""

import json
from typing import Dict, Optional
from ..config import SALARY_DATA_FILE
from ..resources import Region
from ..logger import get_logger

logger = get_logger(__name__)


class SalaryService:
    """
    Handles salary lookups for given job titles and regions.
    """

    def __init__(self, salary_file: str = SALARY_DATA_FILE):
        self.salary_file = salary_file
        self.salary_data = self.load_salary_data()

    def load_salary_data(self) -> Dict[str, Dict[str, Dict]]:
        """
        Load salary data from JSON file.
        Format example:
        {
            "Data Analyst": {
                "africa": {"min": 5000, "max": 15000, "currency": "USD"},
                "western": {"min": 60000, "max": 95000, "currency": "USD"}
            }
        }
        """
        try:
            with open(self.salary_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.debug(f"Loaded salary data from {self.salary_file}")
            return data
        except FileNotFoundError:
            logger.error(f"Salary data file not found: {self.salary_file}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in salary data file: {self.salary_file}")
            return {}

    def get_salary(self, job_title: str, region: Optional[Region] = None) -> Dict:
        """
        Return salary info for a job title.
        If region is None, return both Africa + Western.
        """
        job_key = job_title.strip().lower()
        job_data = self.salary_data.get(job_key, {})
        if region:
            return job_data.get(region.value, {"min": None, "max": None, "currency": None})
        return job_data  # return all regions

# Examp

