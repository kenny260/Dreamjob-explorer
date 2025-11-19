"""
skill_mapper.py
Maps user skills to required job skills and suggests relevant high-school subjects.
"""

from typing import List, Dict
import json
from ..config import SUBJECT_MAPPING_FILE
from ..logger import get_logger

logger = get_logger(__name__)


class SkillMapper:
    """
    Compares user skills to required skills and recommends subjects.
    """

    def __init__(self, mapping_file: str = SUBJECT_MAPPING_FILE):
        self.mapping_file = mapping_file
        self.subject_map = self.load_subject_mapping()

    def load_subject_mapping(self) -> Dict[str, List[str]]:
        """
        Load mapping of skills to high-school subjects from JSON.
        """
        try:
            with open(self.mapping_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.debug(f"Loaded subject mapping from {self.mapping_file}")
            return data
        except FileNotFoundError:
            logger.error(f"Subject mapping file not found: {self.mapping_file}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in subject mapping file: {self.mapping_file}")
            return {}

    def get_missing_skills(self, required_skills: List[str], user_skills: List[str]) -> List[str]:
        """
        Return a list of skills the user does NOT have.
        """
        missing = [skill for skill in required_skills if skill.lower() not in map(str.lower, user_skills)]
        logger.debug(f"Missing skills: {missing}")
        return missing

    def recommend_subjects(self, missing_skills: List[str]) -> List[str]:
        """
        Recommend high-school subjects based on missing skills.
        """
        recommended_subjects = set()
        for skill in missing_skills:
            subjects = self.subject_map.get(skill.lower(), [])
            for subj in subjects:
                recommended_subjects.add(subj)
        logger.debug(f"Recommended subjects: {recommended_subjects}")
        return list(recommended_subjects)

    def analyze(self, required_skills: List[str], user_skills: List[str]) -> Dict:
        """
        Full analysis: missing skills + recommended subjects.
        """
        missing_skills = self.get_missing_skills(required_skills, user_skills)
        recommended_subjects = self.recommend_subjects(missing_skills)
        return {
            "missing_skills": missing_skills,
            "recommended_subjects": recommended_subjects
        }

# Example usage:
# mapper = SkillMapper()
# result = mapper.analyze(required_skills=["Python", "SQL", "Statistics"], user_skills=["Python", "Excel"])
# print(result)

