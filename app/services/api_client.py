"""
api_client.py
Handles external API requests for DreamJob Explorer.
Currently supports ESCO API (skills lookup) and can be extended for Coursera/YouTube.
"""

import requests
from typing import List, Dict, Optional
from ..config import ESCO_API_BASE_URL
from ..logger import get_logger

logger = get_logger(__name__)


class ESCOClient:
    """
    Client for interacting with the ESCO API.
    """

    BASE_URL = ESCO_API_BASE_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def search_occupation(self, job_title: str) -> Optional[Dict]:
        """
        Search ESCO occupations by job title.
        Returns the first matching occupation dictionary or None.
        """
        try:
            url = f"{self.BASE_URL}/resource/occupation"
            params = {"title": job_title, "language": "en"}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and "results" in data and len(data["results"]) > 0:
                logger.debug(f"Found {len(data['results'])} occupations for '{job_title}'")
                return data["results"][0]
            logger.warning(f"No occupations found for '{job_title}'")
            return None
        except requests.RequestException as e:
            logger.error(f"ESCO API request failed: {e}")
            return None

    def get_required_skills(self, occupation_uri: str) -> List[str]:
        """
        Given an ESCO occupation URI, fetch the required skills.
        Returns a list of skill names.
        """
        try:
            url = f"{self.BASE_URL}/resource/occupation/{occupation_uri}/hasSkill"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            skills_data = response.json()
            skills = [skill.get("title", {}).get("en", "") for skill in skills_data]
            logger.debug(f"Found {len(skills)} skills for occupation {occupation_uri}")
            return skills
        except requests.RequestException as e:
            logger.error(f"Failed to fetch skills for {occupation_uri}: {e}")
            return []

# Example usage:
# client = ESCOClient()
# occupation = client.search_occupation("Data Analyst")
# if occupation:
#     skills = client.get_required_skills(occupation["@id"])

