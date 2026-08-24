from models.schemas import (
    CandidateProfile,
    JobProfile,
)

from backend.batch_screening_service import (
    BatchScreeningService,
)


def test_batch_screening():

    candidate1 = CandidateProfile(
        name="John",
        skills=[
            "Python",
            "FastAPI",
        ],
    )

    candidate2 = CandidateProfile(
        name="Alice",
        skills=[
            "Python",
            "FastAPI",
            "Docker",
            "SQL",
        ],
    )

    job = JobProfile(
        job_title="Python Backend Developer",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
            "SQL",
        ],
    )

    service = BatchScreeningService()

    ranked = service.screen_candidates(
        [candidate1, candidate2],
        job,
    )

    assert len(ranked) == 2

    assert ranked[0].candidate.name == "Alice"

    assert ranked[0].match.score == 100.0

    assert ranked[1].candidate.name == "John"

    assert ranked[1].match.score == 50.0


def test_batch_shortlisting():

    candidate1 = CandidateProfile(
        name="John",
        skills=["Python"],
    )

    candidate2 = CandidateProfile(
        name="Alice",
        skills=[
            "Python",
            "FastAPI",
        ],
    )

    job = JobProfile(
        job_title="Backend Developer",
        required_skills=[
            "Python",
            "FastAPI",
        ],
    )

    service = BatchScreeningService()

    ranked = service.screen_candidates(
        [candidate1, candidate2],
        job,
    )

    shortlisted = service.shortlist(
        ranked,
        minimum_score=60.0,
    )

    assert len(shortlisted) == 1

    assert (
        shortlisted[0].candidate.name
        == "Alice"
    )