import re

from models.schemas import Experience


def extract_experience_dates(
    text: str
) -> tuple[str | None, str | None]:
    """
    Extract experience start and end dates.

    Supports:
        May 2025 - July 2025
        May 2025 – July 2025
        Jan 2024 - Present
        2023 - 2024
    """

    pattern = (
        r"([A-Za-z]{3,9}\.?\s+\d{4}|\d{4})"
        r"\s*[-\u2013\u2014]\s*"
        r"([A-Za-z]{3,9}\.?\s+\d{4}|\d{4}|Present|Current)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return (
            match.group(1).strip(),
            match.group(2).strip()
        )

    return None, None

def extract_role(text: str) -> str | None:
    """
    Extract a likely job role from the first few lines.
    """

    role_keywords = [
        "intern",
        "developer",
        "engineer",
        "analyst",
        "manager",
        "designer",
        "consultant",
        "associate"
    ]

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:5]:

        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in role_keywords
        ):
            return line

    return None


def extract_company(text: str) -> str | None:
    """
    Extract a likely company name.

    Prefer the line immediately after a detected role.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    role_keywords = [
        "intern",
        "developer",
        "engineer",
        "analyst",
        "manager",
        "designer",
        "consultant",
        "associate"
    ]

    for index, line in enumerate(lines[:8]):

        lower_line = line.lower()

        is_role = any(
            keyword in lower_line
            for keyword in role_keywords
        )

        if is_role and index + 1 < len(lines):

            company = lines[index + 1]

            # Don't treat another role-like line as company.
            company_lower = company.lower()

            if not any(
                keyword in company_lower
                for keyword in role_keywords
            ):
                return company

    company_keywords = [
        "technologies",
        "technology",
        "solutions",
        "systems",
        "software",
        "limited",
        "ltd",
        "pvt",
        "private",
        "inc",
        "corporation",
        "company"
    ]

    for line in lines[:8]:

        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in company_keywords
        ):
            return line

    return None


def extract_description(text: str) -> str | None:
    """
    Extract bullet points and descriptive lines.
    """

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if re.match(r"^[•▪●\-*]", line):

            cleaned = re.sub(
                r"^[•▪●\-*]\s*",
                "",
                line
            )

            if cleaned:
                lines.append(cleaned)

    if lines:
        return "\n".join(lines)

    return None


def parse_experience_section(
    text: str
) -> list[Experience]:
    """
    Parse an experience section.

    Current version extracts one experience record.
    """

    if not text.strip():
        return []

    start_date, end_date = extract_experience_dates(text)

    role = extract_role(text)

    company = extract_company(text)

    description = extract_description(text)

    experience = Experience(
        company=company,
        role=role,
        start_date=start_date,
        end_date=end_date,
        description=description
    )

    return [experience]