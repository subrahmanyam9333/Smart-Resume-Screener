from typing import Annotated
from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import os

from backend.parser import extract_text_from_pdf
from backend.structured_parser import parse_resume
from backend.screening_service import ScreeningService
from models.schemas import JobProfile
from backend.batch_screening_service import BatchScreeningService
from backend.database import initialize_database, save_candidate

initialize_database()

app = FastAPI(
    title="Smart Resume Screener",
    description="AI-powered resume screening and job matching system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Smart Resume Screener API is running"
    }


@app.post("/extract-resume")
async def extract_resume(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported currently."
        }

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        text = extract_text_from_pdf(temp_path)

        return {
            "filename": file.filename,
            "text": text
        }

    finally:

        os.remove(temp_path)


@app.post("/screen-resume")
async def screen_resume(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    required_skills: str = Form(...),
    preferred_skills: str = Form(""),
    job_description: str = Form(""),
    experience_required: str = Form(""),
    education_required: str = Form("")
):
    """
    Screen a resume against a job description.

    Currently uses deterministic local matching.
    LLM matching can be enabled later.
    """

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported currently."
        }

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        # Extract raw resume text
        text = extract_text_from_pdf(temp_path)

        # Convert resume text into structured profile
        candidate = parse_resume(text)

        save_candidate(candidate)

        # Convert comma-separated skills into lists
        required_skill_list = [
            skill.strip()
            for skill in required_skills.split(",")
            if skill.strip()
        ]

        preferred_skill_list = [
            skill.strip()
            for skill in preferred_skills.split(",")
            if skill.strip()
        ]

        # Build structured job profile
        job = JobProfile(
            job_title=job_title,
            required_skills=required_skill_list,
            preferred_skills=preferred_skill_list,
            experience_required=experience_required or None,
            education_required=education_required or None,
            description=job_description or None
        )

        # Use local matcher for now
        service = ScreeningService(
            use_llm=False
        )

        result = service.screen_candidate(
            candidate,
            job
        )

        return {
            "filename": file.filename,
            "candidate": candidate.model_dump(),
            "job": job.model_dump(),
            "match": result.model_dump()
        }

    finally:

        os.remove(temp_path)


@app.post("/screen-multiple")
async def screen_multiple(
    files: Annotated[list[UploadFile], File(...)],
    job_title: str = Form(...),
    required_skills: str = Form(...),
    preferred_skills: str = Form(""),
    job_description: str = Form(""),
    minimum_score: float = Form(60.0),
    experience_required: str = Form(""),
    education_required: str = Form("")
):
    """
    Screen multiple resumes against one job
    and return ranked candidates.
    """

    candidates = []
    filenames = []

    required_skill_list = [
        skill.strip()
        for skill in required_skills.split(",")
        if skill.strip()
    ]

    preferred_skill_list = [
        skill.strip()
        for skill in preferred_skills.split(",")
        if skill.strip()
    ]

    job = JobProfile(
        job_title=job_title,
        required_skills=required_skill_list,
        preferred_skills=preferred_skill_list,
        experience_required=experience_required or None,
        education_required=education_required or None,
        description=job_description or None
    )   

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            continue

        contents = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        try:

            text = extract_text_from_pdf(
                temp_path
            )
            candidate = parse_resume(text)
            save_candidate(candidate)
            candidates.append(candidate)
            filenames.append(file.filename)

        finally:

            os.remove(temp_path)

    if not candidates:
        return {
            "error": "No valid PDF resumes were uploaded."
        }

    service = BatchScreeningService()

    ranked = service.screen_candidates(
        candidates,
        job,
        minimum_score
    )

    shortlisted = service.shortlist(
        ranked,
        minimum_score
    )

    shortlisted_ids = {
        id(item)
        for item in shortlisted
    }

    results = []

    for rank, item in enumerate(
        ranked,
        start=1
    ):

        candidate = item.candidate
        match = item.match

        results.append({
            "rank": rank,
            "filename": filenames[
                candidates.index(candidate)
            ],
            "name": candidate.name,
            "email": candidate.email,
            "score": match.score,
            "shortlisted": (
                id(item) in shortlisted_ids
            ),
            "matched_skills": (
                match.matched_skills
            ),
            "missing_skills": (
                match.missing_skills
            ),
            "preferred_matched_skills": (
                match.preferred_matched_skills
            ),
            "preferred_missing_skills": (
                match.preferred_missing_skills
            ),
            "experience_score": (
                match.experience_score
            ),
            "education_score": (
                match.education_score
            ),
            "experience_match": (
                match.experience_match
            ),
            "education_match": (
                match.education_match
            ),
            "description_score": (
                match.description_score
            ),
            "description_match": (
                match.description_match
            ),
            "strengths": match.strengths,
            "concerns": match.concerns,
            "justification": (
                match.justification
            )
        })
    
    return {
        "job": job.model_dump(),
        "total_candidates": len(results),
        "shortlisted": len(shortlisted),
        "minimum_score": minimum_score,
        "candidates": results
    }