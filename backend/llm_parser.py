import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from models.schemas import (
    CandidateProfile,
    JobProfile,
    MatchResult,
)

class ResumeLLMParser:

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

    def extract_resume_data(self, resume_text: str) -> CandidateProfile:
        prompt = f"""
You are an expert resume information extraction system.

Extract structured information from the resume below.

IMPORTANT RULES:
1. Only use information explicitly present in the resume.
2. Do not invent skills, experience, education, projects, or certifications.
3. If information is missing, use null for optional fields or an empty list.
4. Keep skills as individual skill names.
5. Keep experience descriptions concise.
6. Return ONLY valid JSON.
7. Follow exactly the requested structure.

Return this JSON structure:

{{
    "name": null,
    "email": null,
    "phone": null,
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "achievements": [],
    "summary": null
}}

Resume:
--------------------
{resume_text}
--------------------
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured information from resumes accurately."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return CandidateProfile.model_validate(data)



class ResumeMatcherLLM:

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

    def build_prompt(
        self,
        candidate: CandidateProfile,
        job: JobProfile,
    ) -> str:

        candidate_data = (
            candidate.model_dump_json(indent=2)
        )

        job_data = (
            job.model_dump_json(indent=2)
        )

        return f"""
You are an expert technical recruiter.

Compare the candidate profile with the job profile.

Evaluate the candidate ONLY using information
present in the supplied data.

Do not invent qualifications or experience.

Give a semantic fit score from 1 to 10.

Consider:
1. Required skills
2. Relevant experience
3. Education
4. Projects
5. Overall relevance

Important:
- A related skill may be considered semantically relevant.
- Do not claim a skill exists if there is no evidence.
- Clearly identify missing requirements.
- Keep the justification concise and specific.

Return ONLY valid JSON in exactly this structure:

{{
    "llm_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "concerns": [],
    "justification": ""
}}

CANDIDATE PROFILE:
--------------------
{candidate_data}
--------------------

JOB PROFILE:
--------------------
{job_data}
--------------------
"""

    def match(
        self,
        candidate: CandidateProfile,
        job: JobProfile,
    ) -> MatchResult:

        prompt = self.build_prompt(
            candidate,
            job,
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical "
                        "recruiter who evaluates "
                        "candidate-job fit accurately."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = (
            response.choices[0]
            .message
            .content
        )

        data = json.loads(content)

        return MatchResult.model_validate(data)