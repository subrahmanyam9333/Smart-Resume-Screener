from models.schemas import (
    CandidateProfile,
    JobProfile,
)

from backend.llm_parser import (
    ResumeMatcherLLM,
)


def test_build_prompt():

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
            "SQL",
        ],
        description=(
            "Develop backend APIs using Python."
        ),
    )

    matcher = ResumeMatcherLLM.__new__(
        ResumeMatcherLLM
    )

    prompt = matcher.build_prompt(
        candidate,
        job,
    )

    assert "John Doe" in prompt

    assert "Python" in prompt

    assert "FastAPI" in prompt

    assert "Python Backend Developer" in prompt

    assert "semantic fit score" in prompt

    assert "llm_score" in prompt

    assert "Return ONLY valid JSON" in prompt