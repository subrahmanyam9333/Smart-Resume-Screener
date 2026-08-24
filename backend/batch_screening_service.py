from models.schemas import (
    CandidateProfile,
    JobProfile,
)

from backend.screening_service import ScreeningService
from backend.ranking_service import (
    RankedCandidate,
    rank_candidates,
    shortlist_candidates,
)


class BatchScreeningService:

    def __init__(self):
        self.screening_service = ScreeningService(
            use_llm=False
        )

    def screen_candidates(
        self,
        candidates: list[CandidateProfile],
        job: JobProfile,
        minimum_score: float = 60.0,
    ) -> list[RankedCandidate]:
        """
        Screen multiple candidates against
        one job and rank them.
        """

        results = [
            self.screening_service.screen_candidate(
                candidate,
                job,
            )
            for candidate in candidates
        ]

        ranked = rank_candidates(
            candidates,
            results,
        )

        return ranked

    def shortlist(
        self,
        ranked_candidates: list[RankedCandidate],
        minimum_score: float = 60.0,
    ) -> list[RankedCandidate]:
        """
        Return candidates meeting the
        minimum shortlist score.
        """

        return shortlist_candidates(
            ranked_candidates,
            minimum_score,
        )