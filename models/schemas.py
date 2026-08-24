from pydantic import BaseModel, Field
from typing import List, Optional


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)

class JobProfile(BaseModel):
    job_title: Optional[str] = None

    required_skills: List[str] = Field(
        default_factory=list
    )

    preferred_skills: List[str] = Field(
        default_factory=list
    )

    experience_required: Optional[str] = None

    education_required: Optional[str] = None

    description: Optional[str] = None

class MatchResult(BaseModel):
    score: float = 0.0

    llm_score: Optional[float] = None

    matched_skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: List[str] = Field(
        default_factory=list
    )

    preferred_matched_skills: List[str] = Field(
        default_factory=list
    )

    preferred_missing_skills: List[str] = Field(
        default_factory=list
    )

    experience_score: float = 0.0

    education_score: float = 0.0

    experience_match: Optional[str] = None

    education_match: Optional[str] = None

    description_score: float = 0.0
    description_match: Optional[str] = None

    strengths: List[str] = Field(
        default_factory=list
    )

    concerns: List[str] = Field(
        default_factory=list
    )

    justification: Optional[str] = None


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[str] = Field(default_factory=list)

    achievements: List[str] = Field(default_factory=list)

    summary: Optional[str] = None