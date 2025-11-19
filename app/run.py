"""
run.py
CLI entry point for DreamJob Explorer.
Collects user input, fetches job skills, analyzes gaps, recommends subjects,
and displays African + Western salaries.
"""

from services.api_client import ESCOClient
from services.skill_mapper import SkillMapper
from services.salary_service import SalaryService
from resources import Region
from logger import get_logger

logger = get_logger(__name__)


def main():
    print("=== DreamJob Explorer ===\n")

    # 1. Get user input
    job_title = input("Enter your dream job title: ").strip()
    user_skills = input("Enter your current skills (comma separated): ").split(",")
    user_skills = [skill.strip() for skill in user_skills if skill.strip()]

    # 2. Fetch occupation info from ESCO API
    esco_client = ESCOClient()
    occupation = esco_client.search_occupation(job_title)
    if not occupation:
        print(f"Sorry, no occupation found for '{job_title}' in ESCO database.")
        return

    required_skills = esco_client.get_required_skills(occupation["@id"])
    if not required_skills:
        print(f"No skill data found for '{job_title}'.")
        return

    # 3. Analyze missing skills and recommend subjects
    mapper = SkillMapper()
    analysis = mapper.analyze(required_skills, user_skills)

    # 4. Load salary info
    salary_service = SalaryService()
    salary_info = salary_service.get_salary(job_title)

    # 5. Display results
    print("\n--- Analysis Results ---")
    print(f"Dream Job: {job_title}")
    print(f"Required Skills: {', '.join(required_skills)}")
    print(f"Your Skills: {', '.join(user_skills)}")
    print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
    print(f"Recommended Subjects: {', '.join(analysis['recommended_subjects'])}")

    print("\n--- Expected Salary ---")
    for region_name in [Region.AFRICA.value, Region.WESTERN.value]:
        region_salary = salary_info.get(region_name, {})
        if region_salary.get("min") is not None:
            print(f"{region_name.capitalize()}: "
                  f"{region_salary['min']} - {region_salary['max']} {region_salary['currency']}")
        else:
            print(f"{region_name.capitalize()}: Data not available")

    print("\nThank you for using DreamJob Explorer!")


if __name__ == "__main__":
    main()

