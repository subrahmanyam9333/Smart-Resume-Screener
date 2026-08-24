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
│   ├── ranking\_service.py
│   └── ...
├── frontend/
│   └── app.py
├── models/
│   └── schemas.py
├── tests/
│   ├── test\_matcher.py
│   ├── test\_batch\_screening\_service.py
│   ├── test\_screening\_service.py
│   ├── test\_resume\_parser.py
│   ├── test\_skills\_parser.py
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

venv\\Scripts\\activate

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



\## 🏗️ System Architecture



The Smart Resume Screener follows a modular client-server architecture.



User

↓

Streamlit Frontend

↓

FastAPI Backend

↓

PDF Resume Parser

↓

Structured Candidate Profile

↓

SQLite Candidate Database

↓

Job Matching Engine

↓

Optional LLM Semantic Matching

↓

Candidate Ranking

↓

Shortlisting and Justification

↓

Screening Results



\### Main Components



Frontend:

Streamlit is used to collect job requirements, upload resumes, and display screening results.



Backend:

FastAPI provides the REST API and coordinates resume processing and screening.



Resume Parser:

PDF resumes are converted into structured candidate profiles containing skills, education, experience, projects, certifications, and achievements.



Matching Engine:

The deterministic matching engine evaluates required skills, preferred skills, experience, education, and job-description similarity.



Database:

SQLite stores parsed candidate information for later retrieval and persistence.



LLM Component:

The project includes an optional OpenAI-based LLM component for semantic resume-job matching and resume information extraction.



\## 🤖 LLM Usage



The LLM component is optional and can provide semantic matching in addition to deterministic rule-based matching.



The system sends the candidate resume information and job requirements to the LLM and requests a structured evaluation.



\### Example LLM Matching Prompt



Compare the following candidate resume with the following job description.



Evaluate the candidate's suitability on a scale from 1 to 10.



Consider:

\- Required skills

\- Preferred skills

\- Relevant experience

\- Education

\- Projects

\- Overall relevance



Return:

\- Match score

\- Matched skills

\- Missing skills

\- Strengths

\- Concerns

\- Short justification



Candidate Resume:

{resume}



Job Description:

{job\_description}



Return the result in structured JSON format.



\### LLM Scoring



The LLM score is converted into a percentage and can be combined with the deterministic matching score.



The deterministic matching system remains available when LLM usage is disabled.



\## 🗄️ Database Storage



The application uses SQLite for persistent candidate storage.



Database:



data/resume\_screener.db



The database stores:



\- Candidate name

\- Email

\- Phone

\- Skills

\- Education

\- Experience

\- Projects

\- Certifications

\- Achievements

\- Summary

\- Creation timestamp



Candidate information is automatically stored when resumes are parsed through the backend.



\## 🔐 Configuration



LLM functionality requires an OpenAI API key.



The API key should be configured using an environment variable:



OPENAI\_API\_KEY



The application can also operate using deterministic matching without an LLM API key.



\## 📦 Deliverables



The project provides:



\- GitHub repository with development commits

\- FastAPI backend

\- Streamlit frontend

\- PDF resume parsing

\- Structured candidate extraction

\- SQLite database storage

\- Multi-factor candidate matching

\- Optional LLM semantic matching

\- Candidate ranking

\- Shortlisting

\- Candidate justification

\- Automated test suite

\- README documentation

\- End-to-end demonstration



\## ✅ Final Validation



The application has been validated using multiple PDF resumes and different combinations of job requirements.



Validated functionality includes:



\- Resume uploading

\- PDF parsing

\- Candidate profile extraction

\- Required skill matching

\- Preferred skill matching

\- Experience matching

\- Education matching

\- Job description matching

\- Candidate ranking

\- Minimum-score shortlisting

\- Candidate strengths and concerns

\- Candidate justification

\- SQLite candidate storage

\- Automated tests

## 🎥 Demo Video

[Watch the 2–3 Minute Smart Resume Screener Demo](https://drive.google.com/file/d/1hDBMmiBGqEZ4VgJKPPmy8gfXffg2OKe-/view?usp=sharing)