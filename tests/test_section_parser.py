from backend.section_parser import (
    detect_section,
    extract_sections
)


SAMPLE_RESUME = """
AJAY PADYALA

EDUCATION

Vellore Institute of Technology – Andhra Pradesh
Bachelor of Technology in Computer Science and Engineering

TECHNICAL SKILLS

Programming Languages: Java
Databases: MySQL

ACHIEVEMENTS

State Brilliance Award
STARS Scheme, VIT-AP

PROFILE

Motivated Computer Science student.
"""


def test_detect_section():

    assert detect_section("EDUCATION") == "education"
    assert detect_section("TECHNICAL SKILLS") == "skills"
    assert detect_section("ACHIEVEMENTS") == "achievements"
    assert detect_section("PROFILE") == "summary"


def test_extract_sections():

    sections = extract_sections(SAMPLE_RESUME)

    assert "education" in sections
    assert "skills" in sections
    assert "achievements" in sections
    assert "summary" in sections

    assert "Vellore Institute" in sections["education"]
    assert "Java" in sections["skills"]
    assert "State Brilliance Award" in sections["achievements"]