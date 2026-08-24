import re


SECTION_ALIASES = {
    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "technologies",
        "technical expertise"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment"
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects"
    ],
    "certifications": [
        "certifications",
        "certificates"
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments"
    ],
    "summary": [
        "summary",
        "profile",
        "professional summary",
        "objective",
        "career objective"
    ]
}


def normalize_heading(line: str) -> str:
    """
    Normalize a possible section heading.
    """

    line = line.strip().lower()

    # Remove common punctuation
    line = re.sub(r"[:\-]+$", "", line)

    # Collapse multiple spaces
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def detect_section(line: str) -> str | None:
    """
    Determine whether a line is a recognized resume section heading.
    """

    normalized = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return section

    return None


def extract_sections(text: str) -> dict[str, str]:
    """
    Split resume text into recognized sections.
    """

    sections = {}

    current_section = None
    current_lines = []

    for line in text.splitlines():

        section = detect_section(line)

        if section:

            # Save previous section
            if current_section is not None:
                sections[current_section] = "\n".join(
                    current_lines
                ).strip()

            current_section = section
            current_lines = []

        elif current_section is not None:

            current_lines.append(line)

    # Save final section
    if current_section is not None:
        sections[current_section] = "\n".join(
            current_lines
        ).strip()

    return sections