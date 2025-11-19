"""
resources.py
Shared constants, enums, and static data used across the app.
"""

from enum import Enum


class Region(Enum):
    """
    Supported salary regions.
    """
    AFRICA = "africa"
    WESTERN = "western"


class EducationLevel(Enum):
    """
    User educational stage — useful for recommending high-school subjects.
    """
    HIGHSCHOOL = "highschool"
    UNDERGRAD = "undergrad"
    GRADUATE = "graduate"


# Default subject mapping keys — these correspond to data/subjects_mapping.json
SUBJECT_CATEGORIES = [
    "mathematics",
    "science",
    "technology",
    "business",
    "humanities",
    "arts",
    "languages"
]

# Default fallback subjects (in case API skill mapping fails)
DEFAULT_SUBJECT_RECOMMENDATIONS = {
    "software developer": ["mathematics", "technology"],
    "data scientist": ["mathematics", "science", "technology"],
    "doctor": ["science"],
    "lawyer": ["humanities", "languages"],
    "civil engineer": ["mathematics", "science", "technology"]
}

