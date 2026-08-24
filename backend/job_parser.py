import re

from models.schemas import JobProfile


COMMON_SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "FastAPI",
    "Flask",
    "Django",
    "Spring Boot",
    "React",
    "Node.js",
    "REST APIs",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Git",
    "GitHub",
    "Machine Learning",
    "Deep Learning",
]


def extract_job_title(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    first_line = lines[0]

    if len(first_line) <= 100:
        return first_line

    return None


def extract_skills(text: str) -> list[str]:
    found = []

    text_lower = text.lower()

    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)

    return found


def extract_experience_required(
    text: str,
) -> str | None:

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"(?:-|to)?\s*"
        r"(\d+(?:\.\d+)?)?\s*"
        r"years?"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    first = match.group(1)
    second = match.group(2)

    if second:
        return f"{first}-{second} years"

    return f"{first} years"


def extract_education_required(
    text: str,
) -> str | None:

    education_keywords = [
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "b.e",
        "m.e",
        "computer science",
    ]

    lines = text.splitlines()

    matches = []

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()

        if any(
            keyword in lower
            for keyword in education_keywords
        ):
            matches.append(clean)

    if matches:
        return matches[0]

    return None


def parse_job_description(
    text: str,
) -> JobProfile:
    """
    Convert raw job description text
    into a structured JobProfile.
    """

    skills = extract_skills(text)

    job_title = extract_job_title(text)

    experience = extract_experience_required(text)

    education = extract_education_required(text)

    return JobProfile(
        job_title=job_title,
        required_skills=skills,
        experience_required=experience,
        education_required=education,
        description=text.strip(),
    )