📄 Smart Resume Screener

AI-powered resume screening and intelligent job matching system.

🚀 Features

Upload multiple PDF resumes

Extract candidate information from resumes

Extract skills, education, experience, projects, and other details

Define required skills

Define preferred skills

Define required experience

Define required education

Add a detailed job description

Calculate candidate skill matching scores

Calculate preferred skill matching

Calculate experience matching

Calculate education matching

Calculate job description matching

Generate an overall candidate score

Rank candidates automatically

Shortlist candidates using a minimum score

Display matched and missing skills

Display candidate strengths and concerns

Provide candidate match justification

FastAPI backend

Streamlit frontend

Automated test suite

🏗️ Project Structure

smart-resume-screener/
├── backend/
│   ├── api.py
│   ├── matcher.py
│   ├── ranking_service.py
│   └── ...
├── frontend/
│   └── app.py
├── models/
│   └── schemas.py
├── tests/
│   ├── test_matcher.py
│   ├── test_batch_screening_service.py
│   ├── test_screening_service.py
│   ├── test_resume_parser.py
│   ├── test_skills_parser.py
│   └── ...
├── requirements.txt
└── README.md

⚙️ Technologies

Python

FastAPI

Streamlit

Pydantic

Pytest

PDF Resume Parsing

Rule-based Candidate Matching

Optional LLM-based Components

📊 Matching System

The system evaluates candidates using multiple qualification factors.

Required Skills

Required skills form the core candidate matching score.

Example:

Python, FastAPI, SQL, Docker

The system identifies:

Matched skills

Missing skills

Required-skill score

Preferred Skills

Preferred skills provide additional qualification information.

Example:

AWS, Git

The system identifies:

Preferred skills matched

Preferred skills missing

Experience

The system evaluates an experience requirement such as:

2+ years

It compares the requirement with the candidate's extracted experience information.

Education

The system compares the candidate's education information with the job's education requirement.

Example:

Bachelor's in Computer Science

Job Description

The system analyzes meaningful terms from the job description and calculates a job-description match score.

🧮 Overall Matching

When additional qualification requirements are provided, the system considers multiple components including:

Required skills

Preferred skills

Experience

Education

Job description

Only the requirements provided by the recruiter are considered in the scoring process.

When no additional qualification requirements are supplied, the original required-skill matching behaviour is preserved.

🏆 Candidate Ranking

Candidates are ranked according to their final match score.

Each candidate result can include:

Candidate name

Resume filename

Match score

Shortlisting status

Matched skills

Missing skills

Preferred skills

Experience match

Education match

Job description match

Strengths

Concerns

Justification

🎯 Shortlisting

A minimum score can be specified by the recruiter.

Example:

Minimum Score: 60%

Candidates meeting or exceeding the minimum score are shortlisted.

🖥️ Running the Application

1. Create a virtual environment

python -m venv venv

2. Activate the virtual environment

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Start the FastAPI backend

uvicorn backend.api:app --reload

5. Start the Streamlit frontend

Open another terminal:

streamlit run frontend/app.py

The application normally runs at:

http://localhost:8501

🧪 Running Tests

Run the complete test suite:

pytest

The project currently contains 41 automated tests covering:

Resume parsing

Structured parsing

Skills parsing

Education parsing

Experience parsing

Project parsing

Job parsing

Matching

Ranking

Batch screening

Screening service

LLM components

Schema validation

🔄 Screening Workflow

Upload PDF Resumes
        ↓
Extract Resume Information
        ↓
Create Candidate Profiles
        ↓
Create Job Profile
        ↓
Match Required Skills
        ↓
Match Preferred Skills
        ↓
Evaluate Experience
        ↓
Evaluate Education
        ↓
Evaluate Job Description
        ↓
Calculate Overall Score
        ↓
Rank Candidates
        ↓
Apply Minimum Score
        ↓
Display Screening Results

📌 Example Job

Job Title:
Python Backend Developer

Required Skills:
Python, FastAPI, SQL, Docker

Preferred Skills:
AWS, Git

Experience Required:
2+ years

Education Required:
Bachelor's in Computer Science

Minimum Score:
60%

📈 Example Screening Result

Candidate: S. PREM CHAND

Match Score: 19.1%

Matched Skills:
Python

Missing Skills:
Docker
FastAPI
SQL

Preferred Skills Matched:
Git

Preferred Skills Missing:
AWS

Experience Match:
0%

Education Match:
0%

Job Description Match:
16%

🧪 Project Validation

The application has been tested with different combinations of job requirements, including:

Required skills only

Required + preferred skills

Required + experience

Required + education

Required + preferred + experience + education

Job description matching

Multiple PDF resumes

Candidate ranking

Minimum-score shortlisting

The complete automated test suite currently passes successfully.

📌 Project Status

Core functionality: Complete ✅

The Smart Resume Screener currently supports resume uploading, candidate profile extraction, job requirement processing, multi-factor candidate matching, ranking, shortlisting, and result visualization.

Final project activities include UI polishing, documentation, Git finalization, and end-to-end deployment validation.