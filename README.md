# 📄 Smart Resume Screener

### AI-Powered Resume Screening & Job Matching Platform

An intelligent resume screening system that extracts structured candidate information from PDF resumes and evaluates candidates against recruiter-defined job requirements.

The platform combines **resume parsing, multi-factor matching, candidate ranking, automated shortlisting, SQLite persistence, and optional LLM-based semantic evaluation**.

---

## 🚀 Key Features

### 📄 Resume Processing

* Upload multiple PDF resumes
* Extract candidate names and contact information
* Extract technical and professional skills
* Extract education details
* Extract work experience
* Extract projects
* Extract certifications
* Extract achievements
* Generate structured candidate profiles

### 💼 Job Configuration

Recruiters can define:

* Job title
* Required skills
* Preferred skills
* Required experience
* Required education
* Detailed job description
* Minimum screening score

### 🎯 Candidate Matching

The system evaluates candidates based on:

* Required skill matching
* Preferred skill matching
* Experience matching
* Education matching
* Job description relevance
* Overall candidate score

### 🏆 Candidate Ranking

Candidates are automatically ranked based on their final matching score.

The screening results provide:

* Candidate name
* Resume filename
* Overall match score
* Matched skills
* Missing skills
* Preferred skills
* Experience evaluation
* Education evaluation
* Job description relevance
* Candidate strengths
* Candidate concerns
* Match justification
* Shortlisting status

---

## 🧠 How the Matching Works

The system uses a multi-factor evaluation approach.

```text
Required Skills
       +
Preferred Skills
       +
Experience
       +
Education
       +
Job Description
       ↓
Overall Candidate Score
       ↓
Candidate Ranking
       ↓
Shortlisting
```

Only the qualification categories provided by the recruiter are considered during scoring.

For example, a recruiter can configure:

```text
Required Skills:
Python, FastAPI, SQL, Docker

Preferred Skills:
AWS, Git

Experience:
2+ years

Education:
Bachelor's in Computer Science

Minimum Score:
60%
```

The system then compares each uploaded resume against these requirements.

---

## 🔍 Screening Process

```text
PDF Resume Upload
        ↓
Resume Text Extraction
        ↓
Candidate Information Extraction
        ↓
Structured Candidate Profile
        ↓
Job Requirement Processing
        ↓
Required Skill Matching
        ↓
Preferred Skill Matching
        ↓
Experience Evaluation
        ↓
Education Evaluation
        ↓
Job Description Matching
        ↓
Overall Score Calculation
        ↓
Candidate Ranking
        ↓
Minimum Score Filtering
        ↓
Screening Results
```

---

## 🏗️ System Architecture

The application follows a modular frontend-backend architecture.

```text
                         USER
                           │
                           ▼
                  Streamlit Frontend
                           │
                           ▼
                     FastAPI Backend
                           │
                           ▼
                  Resume PDF Processing
                           │
                           ▼
                Structured Candidate Data
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        SQLite Database       Matching Engine
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
                 Skills          Experience         Education
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      │
                                      ▼
                           Job Description Match
                                      │
                                      ▼
                         Optional LLM Analysis
                                      │
                                      ▼
                            Final Candidate Score
                                      │
                                      ▼
                              Ranking Engine
                                      │
                                      ▼
                              Shortlisting
                                      │
                                      ▼
                              Results Dashboard
```

---

## 🧩 Main Components

### 🖥️ Streamlit Frontend

Provides the recruiter-facing interface for:

* Entering job requirements
* Uploading resumes
* Starting the screening process
* Viewing candidate rankings
* Reviewing detailed candidate results

### ⚡ FastAPI Backend

Coordinates the application's core processing:

* Resume uploads
* PDF processing
* Candidate profile generation
* Job profile creation
* Screening
* Ranking
* Database persistence

### 📑 Resume Parser

Converts PDF resume content into structured candidate information including:

* Personal information
* Skills
* Education
* Experience
* Projects
* Certifications
* Achievements
* Summary

### 🎯 Matching Engine

The deterministic matching engine evaluates candidates against recruiter-defined requirements.

It supports:

* Required skills
* Preferred skills
* Experience
* Education
* Job description relevance

### 🗄️ SQLite Database

Candidate information is persisted in:

```text
data/resume_screener.db
```

Stored information includes:

* Candidate name
* Email
* Phone
* Skills
* Education
* Experience
* Projects
* Certifications
* Achievements
* Summary
* Creation timestamp

### 🤖 Optional LLM Layer

An optional OpenAI-based component supports:

* Semantic resume interpretation
* Resume information extraction
* Semantic candidate-job matching

The core deterministic screening system can operate without the LLM component.

---

## 🤖 LLM-Based Semantic Matching

When enabled, the LLM receives structured candidate information and job requirements and generates a semantic assessment.

The evaluation considers:

* Required skills
* Preferred skills
* Relevant experience
* Education
* Projects
* Overall relevance

The generated assessment can include:

* Match score
* Matched skills
* Missing skills
* Strengths
* Concerns
* Short justification

The LLM score can be converted into a percentage and combined with deterministic matching results.

---

## 🛠️ Technology Stack

| Category             | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Backend              | FastAPI               |
| Frontend             | Streamlit             |
| Data Validation      | Pydantic              |
| Database             | SQLite                |
| Testing              | Pytest                |
| Resume Input         | PDF                   |
| Matching             | Rule-Based Evaluation |
| Semantic Analysis    | Optional OpenAI LLM   |

---

## 📁 Project Structure

```text
smart-resume-screener/
│
├── backend/
│   ├── api.py
│   ├── matcher.py
│   ├── ranking_service.py
│   └── ...
│
├── frontend/
│   └── app.py
│
├── models/
│   └── schemas.py
│
├── tests/
│   ├── test_matcher.py
│   ├── test_batch_screening_service.py
│   ├── test_screening_service.py
│   ├── test_resume_parser.py
│   ├── test_skills_parser.py
│   └── ...
│
├── data/
│   └── resume_screener.db
│
├── requirements.txt
└── README.md
```

---

## 🧪 Automated Testing

The project includes an automated test suite covering:

* Resume parsing
* Structured candidate parsing
* Skills extraction
* Education extraction
* Experience extraction
* Project extraction
* Job parsing
* Matching
* Ranking
* Batch screening
* Screening service
* LLM components
* Schema validation

Run the complete test suite with:

```bash
pytest
```

The complete automated test suite has been validated successfully.

---

## 📊 Example Screening Result

### Candidate

**S. PREM CHAND**

### Overall Match

**19.1%**

### Matched Skills

* Python

### Missing Skills

* Docker
* FastAPI
* SQL

### Preferred Skills Matched

* Git

### Preferred Skills Missing

* AWS

### Additional Evaluation

| Evaluation            | Score |
| --------------------- | ----: |
| Experience Match      |    0% |
| Education Match       |    0% |
| Job Description Match |   16% |

The system also provides candidate strengths, concerns, and an overall justification for the generated result.

---

## 🎯 Shortlisting

Recruiters can define a minimum score for automatically identifying suitable candidates.

Example:

```text
Minimum Score: 60%
```

Candidates meeting or exceeding the configured score are marked as shortlisted.

This allows recruiters to quickly focus on candidates who satisfy the required qualification criteria.

---

## 🔐 Configuration

The LLM functionality requires an OpenAI API key.

Configure the following environment variable:

```text
OPENAI_API_KEY
```

The deterministic screening pipeline can still operate without an LLM API key.

---

## ✅ Project Validation

The application has been validated using different combinations of job requirements, including:

* Required skills only
* Required + preferred skills
* Required skills + experience
* Required skills + education
* Combined qualification requirements
* Job description matching
* Multiple resume uploads
* Candidate ranking
* Score-based shortlisting

Additional validation covers:

* PDF processing
* Candidate profile generation
* Database persistence
* Automated tests
* Result visualization

---

## 📌 Project Outcome

Smart Resume Screener provides an end-to-end workflow for transforming unstructured PDF resumes into structured candidate profiles and evaluating them against recruiter-defined job requirements.

### The platform combines:

```text
Resume Parsing
      ↓
Candidate Profile Extraction
      ↓
Multi-Factor Matching
      ↓
Optional Semantic Analysis
      ↓
Candidate Ranking
      ↓
Automated Shortlisting
```

The system provides a practical way to reduce manual resume screening effort and quickly identify candidates whose qualifications best match a given job specification.

---

## 🎥 Demo

### ▶️ [Watch the Smart Resume Screener Demo](https://drive.google.com/file/d/1RCDG3GwiXK6wWld_q4aMI2sU4qnoyxRb/view?usp=sharing)

---

## 📌 Project Status

**Core Functionality: Complete ✅**

The project currently supports:

* PDF resume uploading
* Candidate information extraction
* Job requirement processing
* Multi-factor candidate matching
* Candidate ranking
* Candidate shortlisting
* SQLite candidate storage
* Optional LLM semantic matching
* Automated testing
* Screening result visualization
