"""
config.py
Central configuration module for DreamJob Explorer.
Handles environment variables, API base URLs, and file paths.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# API CONFIGURATION
# ---------------------------

# ESCO API (no key required)
ESCO_API_BASE_URL = "https://ec.europa.eu/esco/api"

# Optional APIs (YouTube / Coursera)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
COURSERA_API_KEY = os.getenv("COURSERA_API_KEY", "")

# ---------------------------
# DATA PATHS
# ---------------------------

# Path to static mapping file
SUBJECT_MAPPING_FILE = BASE_DIR / "data" / "subjects_mapping.json"

# Salary dataset (to be created later)
SALARY_DATA_FILE = BASE_DIR / "data" / "salary_data.json"

# ---------------------------
# CACHE SETTINGS
# ---------------------------

CACHE_TTL_SECONDS = 3600  # Cache items for 1 hour

# ---------------------------
# GENERAL CONFIG
# ---------------------------

APP_NAME = "DreamJob Explorer"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

