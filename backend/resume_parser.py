import re

from models.schemas import CandidateProfile


def extract_email(text: str) -> str | None:
    """
    Extract the first email address found in the resume text.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text: str) -> str | None:
    """
    Extract a phone number from the resume text.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_name(text: str) -> str | None:
    """
    Extract the candidate name.

    For the first version, we assume the candidate name
    appears near the beginning of the resume.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        upper_line = line.upper()

        if (
            "@" not in line
            and not re.search(r"\d", line)
            and upper_line not in {
                "EDUCATION",
                "EXPERIENCE",
                "SKILLS",
                "TECHNICAL SKILLS",
                "PROFILE",
                "SUMMARY",
                "PROJECTS",
                "ACHIEVEMENTS",
                "CERTIFICATIONS"
            }
        ):
            return line

    return None


def parse_basic_resume_data(text: str) -> CandidateProfile:
    """
    Extract basic candidate information from resume text.
    """

    return CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text)
    )