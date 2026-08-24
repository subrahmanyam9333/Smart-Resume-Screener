import re

from models.schemas import Project


def extract_technologies(text: str) -> list[str]:
    """
    Extract technologies from lines containing:
    Technologies:
    Tech Stack:
    Tools:
    Built using:
    """

    technologies = []

    patterns = [
        r"(?:Technologies|Technology|Tech Stack|TechStack|Tools|Built using)\s*[:\-]\s*(.+)"
    ]

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                values = match.group(1)

                values = re.split(
                    r",|;|\||/",
                    values
                )

                for value in values:

                    value = value.strip()

                    if value and value not in technologies:
                        technologies.append(value)

    return technologies


def extract_project_name(text: str) -> str | None:
    """
    Extract the first likely project name.

    Usually the project name appears near the beginning
    of the project section.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    # Ignore section headings.
    ignored = {
        "projects",
        "project",
        "academic projects",
        "personal projects"
    }

    for line in lines:

        if line.lower() not in ignored:

            # Don't select bullet points as the name.
            if not re.match(r"^[•▪●\-*]", line):
                return line

    return None


def extract_project_description(text: str) -> str | None:
    """
    Extract bullet-point descriptions while ignoring
    technology/stack lines.
    """

    descriptions = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if not re.match(r"^[•▪●\-*]", line):
            continue

        cleaned = re.sub(
            r"^[•▪●\-*]\s*",
            "",
            line
        )

        if re.match(
            r"(Technologies|Technology|Tech Stack|TechStack|Tools|Built using)\s*:",
            cleaned,
            re.IGNORECASE
        ):
            continue

        if cleaned:
            descriptions.append(cleaned)

    if descriptions:
        return "\n".join(descriptions)

    return None


def parse_project_section(
    text: str
) -> list[Project]:
    """
    Parse a project section.

    Current version extracts one project record.
    """

    if not text.strip():
        return []

    name = extract_project_name(text)

    description = extract_project_description(text)

    technologies = extract_technologies(text)

    project = Project(
        name=name,
        description=description,
        technologies=technologies
    )

    return [project]