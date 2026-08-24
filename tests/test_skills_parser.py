from backend.skills_parser import extract_skills_from_section


def test_extract_skills():

    skills_text = """
    Programming Languages: Java, Python, C++
    Databases: MySQL, MongoDB
    Frameworks: FastAPI, React
    """

    skills = extract_skills_from_section(skills_text)

    assert "Java" in skills
    assert "Python" in skills
    assert "C++" in skills
    assert "MySQL" in skills
    assert "MongoDB" in skills
    assert "FastAPI" in skills
    assert "React" in skills


def test_duplicate_skills_are_removed():

    skills_text = """
    Programming Languages: Java, Python
    Other: Java, Python
    """

    skills = extract_skills_from_section(skills_text)

    assert skills.count("Java") == 1
    assert skills.count("Python") == 1