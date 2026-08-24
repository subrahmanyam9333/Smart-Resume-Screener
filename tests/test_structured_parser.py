from backend.structured_parser import parse_resume


SAMPLE_RESUME = """
AJAY PADYALA
+91 9347569500
ajaypadyala123@gmail.com

EDUCATION

Vellore Institute of Technology - Andhra Pradesh
Bachelor of Technology in Computer Science and Engineering
Sept. 2023 - Present
CGPA: 8.95/10.00

TECHNICAL SKILLS

Programming Languages: Java, Python
DataBases: MySQL, MongoDB

EXPERIENCE

Software Developer Intern
ABC Technologies
May 2025 - July 2025

• Developed REST APIs using Python
• Worked with MySQL

PROJECTS

Smart Resume Screener

• Built an AI-powered resume screening system
• Developed REST API using FastAPI
Technologies: Python, FastAPI, OpenAI

ACHIEVEMENTS

State Brilliance Award
STARS Scheme, VIT-AP

PROFILE

Motivated Computer Science student.
"""


def test_parse_resume():

    candidate = parse_resume(SAMPLE_RESUME)

    # Basic information
    assert candidate.name == "AJAY PADYALA"

    assert candidate.email == (
        "ajaypadyala123@gmail.com"
    )

    assert candidate.phone == (
        "+91 9347569500"
    )

    # Skills
    assert "Java" in candidate.skills

    assert "Python" in candidate.skills

    assert "MySQL" in candidate.skills

    assert "MongoDB" in candidate.skills

    # Education
    assert len(candidate.education) == 1

    assert candidate.education[0].institution == (
        "Vellore Institute of Technology - Andhra Pradesh"
    )

    assert candidate.education[0].degree == (
        "Bachelor of Technology"
    )

    assert candidate.education[0].field_of_study == (
        "Computer Science and Engineering"
    )

    # Experience
    assert len(candidate.experience) == 1

    assert candidate.experience[0].company == (
        "ABC Technologies"
    )

    assert candidate.experience[0].role == (
        "Software Developer Intern"
    )

    assert candidate.experience[0].start_date == (
        "May 2025"
    )

    assert candidate.experience[0].end_date == (
        "July 2025"
    )

    assert "REST APIs" in (
        candidate.experience[0].description
    )

    # Projects
    assert len(candidate.projects) == 1

    assert candidate.projects[0].name == (
        "Smart Resume Screener"
    )

    assert "resume screening" in (
        candidate.projects[0].description
    )

    assert "Python" in (
        candidate.projects[0].technologies
    )

    assert "FastAPI" in (
        candidate.projects[0].technologies
    )

    assert "OpenAI" in (
        candidate.projects[0].technologies
    )