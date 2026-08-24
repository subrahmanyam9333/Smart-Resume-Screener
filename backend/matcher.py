from models.schemas import CandidateProfile, JobProfile


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

    Returns:
        score
        matched skills
        missing skills
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
) -> dict:
    """
    Calculate the overall local match result.
    """

    skill_score, matched, missing = (
        calculate_skill_match(
            candidate,
            job,
        )
    )

    return {
        "score": skill_score,
        "matched_skills": matched,
        "missing_skills": missing,
    }