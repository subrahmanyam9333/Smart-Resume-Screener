import re

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


def calculate_preferred_skill_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[list[str], list[str]]:

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate.skills
    }

    preferred_skills = {
        normalize_skill(skill)
        for skill in job.preferred_skills
    }

    if not preferred_skills:
        return [], []

    matched = candidate_skills.intersection(
        preferred_skills
    )

    missing = preferred_skills.difference(
        candidate_skills
    )

    return (
        sorted(matched),
        sorted(missing),
    )


def extract_years(text: str) -> float | None:
    """
    Extract the first experience value from text.

    Examples:
        '2 years' -> 2.0
        '3+ years' -> 3.0
        '1.5 years' -> 1.5
    """

    if not text:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
        text.lower(),
    )

    if match:
        return float(match.group(1))

    return None


def calculate_experience_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[float, str | None]:
    """
    Compare candidate experience with the job requirement.
    """

    required_years = extract_years(
        job.experience_required or ""
    )

    if required_years is None:
        return 0.0, None

    candidate_years = 0.0

    for experience in candidate.experience:

        date_text = " ".join(
            filter(
                None,
                [
                    experience.start_date,
                    experience.end_date,
                    experience.description,
                ],
            )
        )

        years = extract_years(date_text)

        if years is not None:
            candidate_years += years

    if candidate_years >= required_years:

        return (
            100.0,
            f"Candidate has approximately {candidate_years:g} years of experience; required {required_years:g}+ years.",
        )

    if candidate_years > 0:

        score = (
            candidate_years / required_years
        ) * 100

        return (
            round(min(score, 100.0), 2),
            f"Candidate has approximately {candidate_years:g} years of experience; required {required_years:g}+ years.",
        )

    return (
        0.0,
        f"Candidate experience could not satisfy the required {required_years:g}+ years.",
    )


def calculate_education_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[float, str | None]:
    """
    Compare candidate education with the job requirement.
    """

    requirement = (
        job.education_required or ""
    ).lower().strip()

    if not requirement:
        return 0.0, None

    requirement_words = set(
        re.findall(
            r"[a-z0-9]+",
            requirement,
        )
    )

    best_score = 0.0

    for education in candidate.education:

        candidate_text = " ".join(
            filter(
                None,
                [
                    education.degree,
                    education.field_of_study,
                    education.institution,
                ],
            )
        ).lower()

        candidate_words = set(
            re.findall(
                r"[a-z0-9]+",
                candidate_text,
            )
        )

        if not requirement_words:
            continue

        overlap = (
            requirement_words
            .intersection(candidate_words)
        )

        score = (
            len(overlap)
            / len(requirement_words)
        ) * 100

        best_score = max(
            best_score,
            score,
        )

    if best_score >= 70:

        return (
            round(best_score, 2),
            "Candidate education matches the job requirement.",
        )

    if best_score > 0:

        return (
            round(best_score, 2),
            "Candidate education partially matches the job requirement.",
        )

    return (
        0.0,
        "Candidate education does not match the job requirement.",
    )

def calculate_job_description_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[float, str | None]:
    """
    Compare the job description with the candidate profile.
    """

    description = (
        job.description or ""
    ).lower().strip()

    if not description:
        return 0.0, None

    candidate_parts = []

    candidate_parts.extend(
        candidate.skills
    )

    candidate_parts.extend(
        project.name
        for project in candidate.projects
        if project.name
    )

    candidate_parts.extend(
        project.description
        for project in candidate.projects
        if project.description
    )

    candidate_parts.extend(
        experience.description
        for experience in candidate.experience
        if experience.description
    )

    if candidate.summary:
        candidate_parts.append(
            candidate.summary
        )

    candidate_text = " ".join(
        candidate_parts
    ).lower()

    if not candidate_text:
        return 0.0, (
            "No candidate information available "
            "for job description matching."
        )

    # Extract meaningful words from the job description.
    description_words = set(
        re.findall(
            r"[a-z0-9+#.]+",
            description,
        )
    )

    candidate_words = set(
        re.findall(
            r"[a-z0-9+#.]+",
            candidate_text,
        )
    )

    # Ignore common English words.
    stop_words = {
        "the", "and", "or", "to", "of",
        "a", "an", "in", "for", "with",
        "is", "are", "be", "should",
        "have", "has", "on", "as",
        "this", "that", "from", "we",
        "looking", "candidate", "experience",
        "strong", "skills", "preferred",
        "required",
    }

    description_words -= stop_words

    if not description_words:
        return 0.0, None

    matched_words = (
        description_words.intersection(
            candidate_words
        )
    )

    score = (
        len(matched_words)
        / len(description_words)
    ) * 100

    return (
        round(score, 2),
        f"Candidate matches approximately "
        f"{round(score, 2)}% of the meaningful "
        f"job description terms.",
    )

def calculate_match(
    candidate: CandidateProfile,
    job: JobProfile,
) -> MatchResult:

    skill_score, matched, missing = (
        calculate_skill_match(
            candidate,
            job,
        )
    )

    preferred_matched, preferred_missing = (
        calculate_preferred_skill_match(
            candidate,
            job,
        )
    )

    experience_score, experience_match = (
        calculate_experience_match(
            candidate,
            job,
        )
    )

    education_score, education_match = (
        calculate_education_match(
            candidate,
            job,
        )
    )

    description_score, description_match = (
        calculate_job_description_match(
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

    if experience_match:
        if experience_score >= 100:
            strengths.append(
                "Candidate meets the required experience."
            )
        else:
            concerns.append(
                "Candidate does not fully meet the required experience."
            )

    if education_match:
        if education_score >= 70:
            strengths.append(
                "Candidate education matches the requirement."
            )
        else:
            concerns.append(
                "Candidate education does not fully match the requirement."
            )

    # -------------------------------------------------
    # Calculate final score using only the requirements
    # that are actually provided.
    # -------------------------------------------------

    components = [
        (skill_score, 50.0),
    ]

    if job.preferred_skills:

        preferred_score = (
            len(preferred_matched)
            / len(job.preferred_skills)
        ) * 100

        components.append(
            (preferred_score, 10.0)
        )

    if job.experience_required:

        components.append(
            (experience_score, 20.0)
        )

    if job.education_required:

        components.append(
            (education_score, 10.0)
        )

    if job.description:

        components.append(
            (description_score, 10.0)
        )

    total_weight = sum(
        weight
        for _, weight in components
    )

    final_score = (
        sum(
            score * weight
            for score, weight in components
        )
        / total_weight
    )

    if final_score >= 80:

        justification = (
            "Strong overall match based on qualifications."
        )

    elif final_score >= 50:

        justification = (
            "Moderate overall match with some qualification gaps."
        )

    else:

        justification = (
            "Low overall match with several qualification gaps."
        )

    return MatchResult(
        score=round(final_score, 2),

        matched_skills=matched,
        missing_skills=missing,

        preferred_matched_skills=preferred_matched,
        preferred_missing_skills=preferred_missing,

        experience_score=experience_score,
        education_score=education_score,

        experience_match=experience_match,
        education_match=education_match,

        description_score=description_score,
        description_match=description_match,

        strengths=strengths,
        concerns=concerns,

        justification=justification,
    )

    return MatchResult(
        score=round(final_score, 2),

        matched_skills=matched,

        missing_skills=missing,

        preferred_matched_skills=preferred_matched,

        preferred_missing_skills=preferred_missing,

        experience_score=experience_score,

        education_score=education_score,

        experience_match=experience_match,

        education_match=education_match,

        description_score=description_score,

        description_match=description_match,

        strengths=strengths,

        concerns=concerns,

        justification=justification,
    )

