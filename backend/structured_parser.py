from models.schemas import CandidateProfile

from backend.resume_parser import (
    extract_name,
    extract_email,
    extract_phone
)

from backend.section_parser import extract_sections

from backend.skills_parser import extract_skills_from_section

from backend.education_parser import parse_education_section

from backend.experience_parser import parse_experience_section

from backend.project_parser import parse_project_section


def parse_resume(text: str) -> CandidateProfile:
    """
    Convert raw resume text into a structured CandidateProfile.
    """

    sections = extract_sections(text)

    skills = extract_skills_from_section(
        sections.get("skills", "")
    )

    education = parse_education_section(
        sections.get("education", "")
    )

    experience = parse_experience_section(
        sections.get("experience", "")
    )

    projects = parse_project_section(
        sections.get("projects", "")
    )

    candidate = CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=skills,
        education=education,
        experience=experience,
        projects=projects
    )

    return candidate