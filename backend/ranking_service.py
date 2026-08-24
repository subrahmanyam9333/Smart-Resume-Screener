from models.schemas import (
    CandidateProfile,
    MatchResult,
)


class RankedCandidate:

    def __init__(
        self,
        candidate: CandidateProfile,
        match: MatchResult,
    ):
        self.candidate = candidate
        self.match = match


def rank_candidates(
    candidates: list[CandidateProfile],
    results: list[MatchResult],
) -> list[RankedCandidate]:
    """
    Rank candidates from highest match score
    to lowest match score.
    """

    if len(candidates) != len(results):
        raise ValueError(
            "Candidates and results must have the same length."
        )

    ranked = [
        RankedCandidate(
            candidate,
            result
        )
        for candidate, result
        in zip(candidates, results)
    ]

    ranked.sort(
        key=lambda item: item.match.score,
        reverse=True
    )

    return ranked


def shortlist_candidates(
    ranked_candidates: list[RankedCandidate],
    minimum_score: float = 60.0,
) -> list[RankedCandidate]:
    """
    Return candidates whose match score meets
    the minimum shortlist threshold.
    """

    return [
        item
        for item in ranked_candidates
        if item.match.score >= minimum_score
    ]