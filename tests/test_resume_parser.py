from backend.resume_parser import (
    extract_email,
    extract_phone,
    extract_name,
    parse_basic_resume_data
)


SAMPLE_RESUME = """
AJAY PADYALA
+91 9347569500
ajaypadyala123@gmail.com

EDUCATION

Vellore Institute of Technology – Andhra Pradesh

TECHNICAL SKILLS

Programming Languages: Java
DataBases: MySQL
"""


def test_extract_email():

    email = extract_email(SAMPLE_RESUME)

    assert email == "ajaypadyala123@gmail.com"


def test_extract_phone():

    phone = extract_phone(SAMPLE_RESUME)

    assert phone == "+91 9347569500"


def test_extract_name():

    name = extract_name(SAMPLE_RESUME)

    assert name == "AJAY PADYALA"


def test_parse_basic_resume_data():

    candidate = parse_basic_resume_data(SAMPLE_RESUME)

    assert candidate.name == "AJAY PADYALA"
    assert candidate.email == "ajaypadyala123@gmail.com"
    assert candidate.phone == "+91 9347569500"