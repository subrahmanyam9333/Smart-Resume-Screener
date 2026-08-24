from backend.project_parser import (
    extract_project_name,
    extract_project_description,
    extract_technologies,
    parse_project_section
)


SAMPLE_PROJECT = """
Smart Resume Screener

• Built an AI-powered resume screening system
• Developed REST API using FastAPI
• Created semantic matching between resumes and job descriptions
Technologies: Python, FastAPI, OpenAI

"""


def test_extract_project_name():

    name = extract_project_name(
        SAMPLE_PROJECT
    )

    assert name == "Smart Resume Screener"


def test_extract_project_description():

    description = extract_project_description(
        SAMPLE_PROJECT
    )

    assert "AI-powered resume screening system" in description

    assert "REST API using FastAPI" in description

    assert "semantic matching" in description


def test_extract_technologies():

    technologies = extract_technologies(
        SAMPLE_PROJECT
    )

    assert "Python" in technologies
    assert "FastAPI" in technologies
    assert "OpenAI" in technologies


def test_parse_project_section():

    projects = parse_project_section(
        SAMPLE_PROJECT
    )

    assert len(projects) == 1

    assert projects[0].name == (
        "Smart Resume Screener"
    )

    assert "resume screening" in (
        projects[0].description
    )

    assert "Python" in projects[0].technologies

    assert "FastAPI" in projects[0].technologies

    assert "OpenAI" in projects[0].technologies