from models.schemas import CandidateProfile


def test_candidate_profile():

    candidate = CandidateProfile(
        name="John Doe",
        email="john@example.com",
        skills=["Python", "FastAPI", "SQL"]
    )

    assert candidate.name == "John Doe"
    assert candidate.email == "john@example.com"
    assert "Python" in candidate.skills