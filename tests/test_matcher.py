from models.schemas import CandidateProfile, JobProfile

from backend.matcher import (
    normalize_skill,
    calculate_skill_match,
    calculate_match,
)


def test_normalize_skill():

    assert normalize_skill(" Python ") == "python"

    assert normalize_skill("FASTAPI") == "fastapi"


def test_calculate_skill_match():

    candidate = CandidateProfile(
        skills=[
            "Python",
            "FastAPI",
            "MySQL",
        ]
    )

    job = JobProfile(
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
            "SQL",
        ]
    )

    score, matched, missing = (
        calculate_skill_match(
            candidate,
            job,
        )
    )

    assert score == 50.0

    assert "python" in matched
    assert "fastapi" in matched

    assert "docker" in missing
    assert "sql" in missing


def test_no_required_skills():

    candidate = CandidateProfile(
        skills=["Python"]
    )

    job = JobProfile(
        required_skills=[]
    )

    score, matched, missing = (
        calculate_skill_match(
            candidate,
            job,
        )
    )

    assert score == 0.0
    assert matched == []
    assert missing == []


def test_calculate_match():

    candidate = CandidateProfile(
        skills=[
            "Python",
            "FastAPI",
        ]
    )

    job = JobProfile(
        required_skills=[
            "Python",
            "FastAPI",
        ]
    )

    result = calculate_match(
        candidate,
        job,
    )

    assert result["score"] == 100.0

    assert len(result["matched_skills"]) == 2

    assert result["missing_skills"] == []