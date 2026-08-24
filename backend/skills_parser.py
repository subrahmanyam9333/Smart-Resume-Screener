import re


def clean_skill(skill: str) -> str:
    """
    Clean an individual skill name.
    """

    skill = skill.strip()

    # Remove common bullet characters
    skill = re.sub(r"^[•▪●\-*]+\s*", "", skill)

    # Remove unnecessary spaces
    skill = re.sub(r"\s+", " ", skill)

    return skill.strip()


def extract_skills_from_section(section_text: str) -> list[str]:
    """
    Extract individual skills from a skills section.

    Supports formats such as:

    Programming Languages: Java, Python, C++
    Databases: MySQL, MongoDB
    Frameworks: FastAPI, React
    """

    skills = []

    for line in section_text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Example:
        # Programming Languages: Java, Python
        if ":" in line:
            _, values = line.split(":", 1)
        else:
            values = line

        # Split comma/semicolon/pipe separated skills
        parts = re.split(r"[,;|]", values)

        for part in parts:

            skill = clean_skill(part)

            if skill and skill not in skills:
                skills.append(skill)

    return skills