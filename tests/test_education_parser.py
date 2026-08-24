from backend.education_parser import (
    extract_grade,
    extract_dates,
    extract_degree_and_field,
    extract_institution,
    parse_education_section
)


SAMPLE_EDUCATION = """
Vellore Institute of Technology – Andhra Pradesh
Sept. 2023 – Present
Bachelor of Technology in Computer Science and Engineering
CGPA: 8.95/10.00

Government Junior College, Kanigiri
Jun. 2021 – May 2023
Intermediate (MPC)
Marks: 947 / 1000
"""


def test_extract_grade():

    grade = extract_grade(
        "Bachelor of Technology\nCGPA: 8.95/10.00"
    )

    assert grade == "8.95/10.00"


def test_extract_dates():

    start, end = extract_dates(
        "Sept. 2023 – Present"
    )

    assert start == "Sept. 2023"
    assert end == "Present"


def test_extract_degree_and_field():

    degree, field = extract_degree_and_field(
        "Bachelor of Technology in Computer Science and Engineering"
    )

    assert degree == "Bachelor of Technology"
    assert field == "Computer Science and Engineering"


def test_extract_institution():

    institution = extract_institution(
        "Vellore Institute of Technology – Andhra Pradesh"
    )

    assert institution == (
        "Vellore Institute of Technology – Andhra Pradesh"
    )


def test_parse_education_section():

    education = parse_education_section(
        SAMPLE_EDUCATION
    )

    assert len(education) == 1

    assert education[0].institution == (
        "Vellore Institute of Technology – Andhra Pradesh"
    )

    assert education[0].degree == "Bachelor of Technology"

    assert education[0].field_of_study == (
        "Computer Science and Engineering"
    )

    assert education[0].start_date == "Sept. 2023"

    assert education[0].end_date == "Present"

    assert education[0].grade == "8.95/10.00"