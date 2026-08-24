import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from models.schemas import CandidateProfile


class ResumeLLMParser:

    def __init__(self, api_key: str):
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