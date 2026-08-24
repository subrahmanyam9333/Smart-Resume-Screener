from backend.experience_parser import (
    extract_experience_dates,
    extract_role,
    extract_company,
    extract_description,
    parse_experience_section
)


SAMPLE_EXPERIENCE = """
Software Developer Intern
ABC Technologies
May 2025 – July 2025

• Developed REST APIs using Python
• Worked with MySQL
• Improved application performance
"""


def test_extract_experience_dates():

    start, end = extract_experience_dates(
        "May 2025 – July 2025"
    )

    assert start == "May 2025"
    assert end == "July 2025"


def test_extract_role():

    role = extract_role(
        SAMPLE_EXPERIENCE
    )

    assert role == "Software Developer Intern"


def test_extract_company():

    company = extract_company(
        SAMPLE_EXPERIENCE
    )

    assert company == "ABC Technologies"


def test_extract_description():

    description = extract_description(
        SAMPLE_EXPERIENCE
    )

    assert "Developed REST APIs using Python" in description
    assert "Worked with MySQL" in description
    assert "Improved application performance" in description


def test_parse_experience_section():

    experience = parse_experience_section(
        SAMPLE_EXPERIENCE
    )

    assert len(experience) == 1

    assert experience[0].company == "ABC Technologies"

    assert experience[0].role == (
        "Software Developer Intern"
    )

    assert experience[0].start_date == "May 2025"

    assert experience[0].end_date == "July 2025"

    assert "REST APIs" in experience[0].description