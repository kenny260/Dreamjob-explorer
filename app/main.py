"""
main.py
FastAPI web application for DreamJob Explorer.
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.api_client import ESCOClient
from services.skill_mapper import SkillMapper
from services.salary_service import SalaryService
from resources import Region
from logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="DreamJob Explorer")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="app/templates")

# Initialize services
esco_client = ESCOClient()
skill_mapper = SkillMapper()
salary_service = SalaryService()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the home page with form.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def analyze(
    request: Request,
    job_title: str = Form(...),
    user_skills: str = Form(...)
):
    """
    Handle form submission, run skill analysis and salary lookup.
    """
    user_skills_list = [skill.strip() for skill in user_skills.split(",") if skill.strip()]

    # 1. Fetch occupation & required skills
    occupation = esco_client.search_occupation(job_title)
    if occupation:
        required_skills = esco_client.get_required_skills(occupation["@id"])
    else:
        required_skills = []

    if not required_skills:
        result = {"error": f"No skill data found for '{job_title}'."}
        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    # 2. Skill mapping
    analysis = skill_mapper.analyze(required_skills, user_skills_list)

    # 3. Salary info
    salary_info = salary_service.get_salary(job_title)

    result = {
        "job_title": job_title,
        "required_skills": required_skills,
        "user_skills": user_skills_list,
        "missing_skills": analysis["missing_skills"],
        "recommended_subjects": analysis["recommended_subjects"],
        "salary_info": salary_info
    }

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

