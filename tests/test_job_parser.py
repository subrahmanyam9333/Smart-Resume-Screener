from backend.job_parser import (
    extract_job_title,
    extract_skills,
    extract_experience_required,
    extract_education_required,
    parse_job_description,
)


SAMPLE_JOB = """
Python Backend Developer

Requirements:
Strong Python programming
Experience with FastAPI
Knowledge of REST APIs
SQL database experience

Preferred:
Docker
AWS

Education:
Bachelor's degree in Computer Science

Experience:
1-2 years
"""


def test_extract_job_title():

    title = extract_job_title(SAMPLE_JOB)

    assert title == "Python Backend Developer"


def test_extract_skills():

    skills = extract_skills(SAMPLE_JOB)

    assert "Python" in skills
    assert "FastAPI" in skills
    assert "REST APIs" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills


def test_extract_experience():

    experience = extract_experience_required(
        SAMPLE_JOB
    )

    assert experience == "1-2 years"


def test_extract_education():

    education = extract_education_required(
        SAMPLE_JOB
    )

    assert education == (
        "Bachelor's degree in Computer Science"
    )


def test_parse_job_description():

    job = parse_job_description(SAMPLE_JOB)

    assert job.job_title == (
        "Python Backend Developer"
    )

    assert "Python" in job.required_skills
    assert "FastAPI" in job.required_skills

    assert job.experience_required == "1-2 years"

    assert job.education_required == (
        "Bachelor's degree in Computer Science"
    )

    assert job.description.strip() == (
        SAMPLE_JOB.strip()
    )