from models.schemas import (
    CandidateProfile,
    MatchResult,
)

from backend.ranking_service import (
    rank_candidates,
    shortlist_candidates,
)


def test_rank_candidates():

    candidate1 = CandidateProfile(
        name="John"
    )

    candidate2 = CandidateProfile(
        name="Alice"
    )

    result1 = MatchResult(
        score=40.0,
        justification="Low match."
    )

    result2 = MatchResult(
        score=90.0,
        justification="Strong match."
    )

    ranked = rank_candidates(
        [candidate1, candidate2],
        [result1, result2],
    )

    assert ranked[0].candidate.name == "Alice"
    assert ranked[0].match.score == 90.0

    assert ranked[1].candidate.name == "John"
    assert ranked[1].match.score == 40.0


def test_shortlist_candidates():

    candidate1 = CandidateProfile(
        name="John"
    )

    candidate2 = CandidateProfile(
        name="Alice"
    )

    result1 = MatchResult(
        score=40.0
    )

    result2 = MatchResult(
        score=85.0
    )

    ranked = rank_candidates(
        [candidate1, candidate2],
        [result1, result2],
    )

    shortlisted = shortlist_candidates(
        ranked,
        minimum_score=60.0
    )

    assert len(shortlisted) == 1

    assert (
        shortlisted[0].candidate.name
        == "Alice"
    )