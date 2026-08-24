from models.schemas import (
    CandidateProfile,
    JobProfile,
)

from backend.screening_service import (
    ScreeningService,
)


def test_screen_candidate_without_llm():

    candidate = CandidateProfile(
        name="John Doe",
        skills=[
            "Python",
            "FastAPI",
            "MySQL",
        ],
    )

    job = JobProfile(
        job_title="Python Backend Developer",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
            "AWS",
        ],
    )

    service = ScreeningService(
        use_llm=False
    )

    result = service.screen_candidate(
        candidate,
        job,
    )

    assert result.score == 50.0

    assert "python" in result.matched_skills
    assert "fastapi" in result.matched_skills

    assert "aws" in result.missing_skills
    assert "docker" in result.missing_skills

    assert result.llm_score is None