import re

from models.schemas import Education


def extract_grade(text: str) -> str | None:
    """
    Extract CGPA, GPA, percentage, or marks information.
    """

    patterns = [
        r"(?:CGPA|GPA)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?\s*/\s*[0-9]+(?:\.[0-9]+)?)",
        r"(?:CGPA|GPA)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)",
        r"([0-9]+(?:\.[0-9]+)?\s*%)",
        r"(?:Marks|Score)\s*[:\-]?\s*([0-9]+\s*/\s*[0-9]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def extract_dates(text: str) -> tuple[str | None, str | None]:
    """
    Extract a start and end date.

    Examples:
        2023 - 2026
        Sept. 2023 - Present
        Jun. 2021 – May 2023
    """

    month = (
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
        r"\.?"
    )

    date = rf"(?:{month}\s+)?(?:\d{{4}}|Present|Current)"

    pattern = rf"({date})\s*[-–—]\s*({date})"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return (
            match.group(1).strip(),
            match.group(2).strip()
        )

    return None, None


def extract_degree_and_field(
    text: str
) -> tuple[str | None, str | None]:
    """
    Extract degree and field of study.
    """

    patterns = [
        r"(Bachelor of Technology)\s+in\s+(.+)",
        r"(Bachelor of Engineering)\s+in\s+(.+)",
        r"(Bachelor of Science)\s+in\s+(.+)",
        r"(Master of Technology)\s+in\s+(.+)",
        r"(Master of Engineering)\s+in\s+(.+)",
        r"(Master of Science)\s+in\s+(.+)",
        r"(Bachelor of Computer Applications)\s+in\s+(.+)",
        r"(Master of Computer Applications)\s+in\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            degree = match.group(1).strip()
            field = match.group(2).strip()

            field = re.split(
                r"\n|CGPA|GPA|Marks|Score",
                field,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0].strip()

            return degree, field

    return None, None


def extract_institution(text: str) -> str | None:
    """
    Attempt to identify the educational institution.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    institution_keywords = [
        "university",
        "institute",
        "college",
        "school"
    ]

    for line in lines:
        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in institution_keywords
        ):
            return line

    return None


def parse_education_section(text: str) -> list[Education]:
    """
    Parse an education section into Education objects.
    """

    if not text.strip():
        return []

    degree, field = extract_degree_and_field(text)

    start_date, end_date = extract_dates(text)

    grade = extract_grade(text)

    institution = extract_institution(text)

    education = Education(
        institution=institution,
        degree=degree,
        field_of_study=field,
        start_date=start_date,
        end_date=end_date,
        grade=grade
    )

    return [education]