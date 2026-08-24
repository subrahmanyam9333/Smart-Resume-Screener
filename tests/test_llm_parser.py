from models.schemas import CandidateProfile


def test_llm_output_schema():

    llm_output = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+919876543210",
        "skills": [
            "Python",
            "FastAPI",
            "SQL"
        ],
        "education": [
            {
                "institution": "ABC University",
                "degree": "B.Tech",
                "field_of_study": "Computer Science",
                "start_date": "2022",
                "end_date": "2026",
                "grade": "8.5"
            }
        ],
        "experience": [],
        "projects": [],
        "certifications": [],
        "achievements": [],
        "summary": "Computer Science student"
    }

    candidate = CandidateProfile.model_validate(llm_output)

    assert candidate.name == "John Doe"
    assert "Python" in candidate.skills
    assert candidate.education[0].degree == "B.Tech"