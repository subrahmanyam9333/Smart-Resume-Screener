from models.schemas import CandidateProfile

from backend.resume_parser import (
    extract_name,
    extract_email,
    extract_phone
)

from backend.section_parser import extract_sections

from backend.skills_parser import extract_skills_from_section


def parse_resume(text: str) -> CandidateProfile:
    """
    Convert raw resume text into a structured CandidateProfile.
    """

    sections = extract_sections(text)

    skills = extract_skills_from_section(
        sections.get("skills", "")
    )

    candidate = CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=skills
    )

    return candidate