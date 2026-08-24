from models.schemas import (
    CandidateProfile,
    JobProfile,
    MatchResult,
)

from backend.matcher import calculate_match
from backend.llm_parser import ResumeMatcherLLM


class ScreeningService:
    """
    Coordinates candidate screening using
    deterministic matching and optional LLM matching.
    """

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

        self.llm_matcher = None

        if self.use_llm:
            self.llm_matcher = ResumeMatcherLLM()

    def screen_candidate(
        self,
        candidate: CandidateProfile,
        job: JobProfile,
    ) -> MatchResult:
        """
        Screen a candidate against a job.
        """

        local_result = calculate_match(
            candidate,
            job,
        )

        if not self.use_llm:
            return local_result

        llm_result = self.llm_matcher.match(
            candidate,
            job,
        )

        return self._combine_results(
            local_result,
            llm_result,
        )

    def _combine_results(
        self,
        local_result: MatchResult,
        llm_result: MatchResult,
    ) -> MatchResult:
        """
        Combine deterministic and LLM results.
        """

        llm_score = llm_result.llm_score

        if llm_score is None:
            final_score = local_result.score
        else:
            llm_percentage = llm_score * 10

            final_score = (
                local_result.score * 0.5
                + llm_percentage * 0.5
            )

        matched_skills = sorted(
            set(
                local_result.matched_skills
                + llm_result.matched_skills
            )
        )

        missing_skills = sorted(
            set(
                local_result.missing_skills
                + llm_result.missing_skills
            )
        )

        strengths = (
            local_result.strengths
            + llm_result.strengths
        )

        concerns = (
            local_result.concerns
            + llm_result.concerns
        )

        justification = (
            llm_result.justification
            or local_result.justification
        )

        return MatchResult(
            score=round(final_score, 2),
            llm_score=llm_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            strengths=strengths,
            concerns=concerns,
            justification=justification,
        )