from models.schemas import (
    CandidateProfile,
    JobProfile,
    MatchResult,
)


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """

    return skill.lower().strip()


def calculate_skill_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[float, list[str], list[str]]:
    """
    Calculate how well candidate skills match
    the job requirements.
    """

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate.skills
    }

    required_skills = {
        normalize_skill(skill)
        for skill in job.required_skills
    }

    if not required_skills:
        return 0.0, [], []

    matched = candidate_skills.intersection(
        required_skills
    )

    missing = required_skills.difference(
        candidate_skills
    )

    score = (
        len(matched) / len(required_skills)
    ) * 100

    return (
        round(score, 2),
        sorted(matched),
        sorted(missing),
    )


def calculate_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> MatchResult:
    """
    Calculate a deterministic local match result.
    """

    score, matched, missing = (
        calculate_skill_match(
            candidate,
            job,
        )
    )

    strengths = [
        f"Candidate matches required skill: {skill}"
        for skill in matched
    ]

    concerns = [
        f"Candidate is missing required skill: {skill}"
        for skill in missing
    ]

    if score >= 80:
        justification = (
            "Strong match based on required skills."
        )

    elif score >= 50:
        justification = (
            "Moderate match based on required skills."
        )

    else:
        justification = (
            "Low match based on required skills."
        )

    return MatchResult(
        score=score,
        matched_skills=matched,
        missing_skills=missing,
        strengths=strengths,
        concerns=concerns,
        justification=justification,
    )