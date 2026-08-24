from backend.structured_parser import parse_resume


SAMPLE_RESUME = """
AJAY PADYALA
+91 9347569500
ajaypadyala123@gmail.com

EDUCATION

Vellore Institute of Technology – Andhra Pradesh
Bachelor of Technology in Computer Science and Engineering

TECHNICAL SKILLS

Programming Languages: Java
DataBases: MySQL

ACHIEVEMENTS

State Brilliance Award
STARS Scheme, VIT-AP

PROFILE

Motivated Computer Science student.
"""


def test_parse_resume():

    candidate = parse_resume(SAMPLE_RESUME)

    assert candidate.name == "AJAY PADYALA"

    assert candidate.email == "ajaypadyala123@gmail.com"

    assert candidate.phone == "+91 9347569500"

    assert "Java" in candidate.skills

    assert "MySQL" in candidate.skills