\# Smart Resume Screening \& Job Matching Platform



An automated resume evaluation system that extracts candidate information from PDF resumes and compares applicants against recruiter-defined job requirements.



The application combines structured resume parsing, rule-based qualification matching, candidate ranking, shortlisting, SQLite persistence, and optional LLM-assisted semantic evaluation.



\---



\## ✨ What the Application Does



The system helps recruiters evaluate multiple resumes against a single job opening.



\### Candidate Processing

\- Upload multiple PDF resumes

\- Extract candidate names and contact information

\- Identify technical and professional skills

\- Extract education details

\- Extract experience information

\- Extract projects, certifications, and achievements

\- Build structured candidate profiles



\### Job Configuration

Recruiters can specify:



\- Job title

\- Mandatory skills

\- Additional/preferred skills

\- Required experience

\- Required educational qualification

\- Detailed job description

\- Minimum screening score



\### Candidate Evaluation

Each applicant is evaluated using several criteria:



\- Mandatory skill coverage

\- Preferred skill coverage

\- Experience compatibility

\- Education compatibility

\- Job-description relevance

\- Overall qualification score



The results are then ranked automatically and candidates meeting the configured threshold are shortlisted.



\---



\## 🧠 Matching Approach



The screening engine uses a multi-factor evaluation strategy.



\### 1. Mandatory Skills



Mandatory skills represent the core technical requirements of a position.



For example:



```text

Python, FastAPI, SQL, Docker

The system determines:



Skills found in the resume

Skills absent from the resume

Mandatory-skill matching score

2\. Preferred Skills



Preferred skills are additional qualifications that can improve a candidate's suitability.



Example:



AWS, Git



The system reports both matched and unmatched preferred skills.



3\. Experience



A recruiter can specify requirements such as:



2+ years



The candidate's extracted experience is compared against the requirement.



4\. Education



The system evaluates the candidate's educational background against the specified qualification.



Example:



Bachelor's in Computer Science

5\. Job Description Similarity



Important terms from the complete job description are compared with the candidate information to estimate relevance.



📊 Final Candidate Score



The final screening result can incorporate:



Mandatory Skills

&#x20;      +

Preferred Skills

&#x20;      +

Experience

&#x20;      +

Education

&#x20;      +

Job Description Relevance

&#x20;      ↓

Overall Match Score



Only the qualification categories supplied by the recruiter are considered.



If optional qualification fields are not provided, the system can continue using the core required-skill matching behavior.



🏆 Candidate Ranking \& Shortlisting



After evaluation, candidates are ordered according to their final score.



Each result can contain:



Candidate name

Resume filename

Overall match percentage

Shortlisting decision

Matched mandatory skills

Missing mandatory skills

Preferred skills matched

Preferred skills missing

Experience evaluation

Education evaluation

Job-description relevance

Candidate strengths

Potential concerns

Final justification

Example Threshold

Minimum Score: 60%



Candidates scoring at least the configured threshold are marked as shortlisted.



🏗️ Application Architecture



The application follows a modular frontend-backend architecture.



&#x20;                   USER

&#x20;                     |

&#x20;                     v

&#x20;             Streamlit Interface

&#x20;                     |

&#x20;                     v

&#x20;                FastAPI API

&#x20;                     |

&#x20;                     v

&#x20;              PDF Text Extraction

&#x20;                     |

&#x20;                     v

&#x20;            Structured Resume Data

&#x20;                     |

&#x20;            +--------+--------+

&#x20;            |                 |

&#x20;            v                 v

&#x20;       SQLite Storage     Matching Engine

&#x20;                              |

&#x20;                   +----------+----------+

&#x20;                   |          |          |

&#x20;                   v          v          v

&#x20;                Skills    Experience   Education

&#x20;                   |          |          |

&#x20;                   +----------+----------+

&#x20;                              |

&#x20;                              v

&#x20;                   Job Description Match

&#x20;                              |

&#x20;                              v

&#x20;                   Optional LLM Analysis

&#x20;                              |

&#x20;                              v

&#x20;                      Final Candidate Score

&#x20;                              |

&#x20;                              v

&#x20;                        Ranking Engine

&#x20;                              |

&#x20;                              v

&#x20;                      Shortlist Candidates

&#x20;                              |

&#x20;                              v

&#x20;                        Results Dashboard

🧩 Main Components

Streamlit Frontend



Provides the recruiter-facing interface for:



Entering job requirements

Uploading resumes

Starting screening

Viewing candidate rankings

Reviewing detailed candidate results

FastAPI Backend



Acts as the application API and coordinates:



Resume uploads

PDF processing

Candidate profile generation

Job profile creation

Screening

Ranking

Database persistence

Resume Processing



PDF resume content is converted into structured information such as:



Personal Information

Skills

Education

Experience

Projects

Certifications

Achievements

Summary

Matching Engine



The deterministic matching layer evaluates candidate suitability across the configured requirements.



SQLite Database



Candidate profiles are persisted in:



data/resume\_screener.db

LLM Layer



An optional OpenAI-based component is included for:



Semantic resume interpretation

Resume information extraction

Semantic candidate-job matching



The application does not depend on the LLM component for its basic deterministic screening functionality.



🤖 Optional LLM Evaluation



The project includes an optional LLM-based semantic matching component.



The LLM receives candidate information and job requirements and produces a structured assessment.



Example Evaluation Prompt

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



The LLM score can be converted into a percentage and combined with deterministic matching results when LLM screening is enabled.



🗄️ Candidate Data Persistence



SQLite is used for persistent candidate storage.



Database location:



data/resume\_screener.db



Stored information includes:



Candidate name

Email

Phone

Skills

Education

Experience

Projects

Certifications

Achievements

Summary

Creation timestamp



Candidate information is stored when resumes are processed through the backend.



📁 Repository Layout

smart-resume-screener/

│

├── backend/

│   ├── api.py

│   ├── matcher.py

│   ├── ranking\_service.py

│   └── ...

│

├── frontend/

│   └── app.py

│

├── models/

│   └── schemas.py

│

├── tests/

│   ├── test\_matcher.py

│   ├── test\_batch\_screening\_service.py

│   ├── test\_screening\_service.py

│   ├── test\_resume\_parser.py

│   ├── test\_skills\_parser.py

│   └── ...

│

├── data/

│   └── resume\_screener.db

│

├── requirements.txt

└── README.md

🛠️ Technology Stack

Area	Technology

Programming Language	Python

API Layer	FastAPI

User Interface	Streamlit

Data Validation	Pydantic

Database	SQLite

Testing	Pytest

Resume Input	PDF

Core Matching	Rule-based evaluation

Semantic Matching	Optional OpenAI LLM

🚀 Running the Project

Step 1 — Create a virtual environment

python -m venv venv

Step 2 — Activate it



Windows:



venv\\Scripts\\activate

Step 3 — Install dependencies

pip install -r requirements.txt

Step 4 — Start the API server

uvicorn backend.api:app --reload

Step 5 — Start the frontend



Open another terminal:



streamlit run frontend/app.py



The Streamlit application normally becomes available at:



http://localhost:8501

🧪 Automated Testing



Run the complete test suite with:



pytest



The project contains tests covering areas such as:



Resume parsing

Structured candidate parsing

Skills extraction

Education extraction

Experience extraction

Project extraction

Job parsing

Matching

Ranking

Batch screening

Screening service

LLM components

Schema validation



The complete automated test suite has been validated successfully.



🔄 End-to-End Screening Flow

1\. Recruiter enters job requirements

&#x20;               ↓

2\. Recruiter uploads PDF resumes

&#x20;               ↓

3\. Resume text is extracted

&#x20;               ↓

4\. Candidate profiles are generated

&#x20;               ↓

5\. Job requirements are structured

&#x20;               ↓

6\. Mandatory skills are evaluated

&#x20;               ↓

7\. Preferred skills are evaluated

&#x20;               ↓

8\. Experience is evaluated

&#x20;               ↓

9\. Education is evaluated

&#x20;               ↓

10\. Job description relevance is calculated

&#x20;               ↓

11\. Overall score is generated

&#x20;               ↓

12\. Candidates are ranked

&#x20;               ↓

13\. Minimum score is applied

&#x20;               ↓

14\. Results and explanations are displayed

📌 Example Screening Configuration

Position

Python Backend Developer

Required Skills

Python, FastAPI, SQL, Docker

Preferred Skills

AWS, Git

Experience

2+ years

Education

Bachelor's in Computer Science

Minimum Score

60%

📈 Example Result



One example screening output is:



Candidate: S. PREM CHAND



Overall Match: 19.1%



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



The dashboard also provides strengths, concerns, and an overall justification for the generated result.



🔐 LLM Configuration



LLM functionality requires an OpenAI API key.



Configure it through the following environment variable:



OPENAI\_API\_KEY



The deterministic screening pipeline can operate without an LLM API key.



✅ Validation



The application has been tested across different screening configurations, including:



Mandatory skills only

Mandatory + preferred skills

Mandatory skills + experience

Mandatory skills + education

Combined qualification requirements

Job-description matching

Multiple resume uploads

Candidate ranking

Score-based shortlisting



Additional validation covers:



PDF processing

Candidate profile generation

Database persistence

Automated tests

Result visualization

🎯 Project Outcome



Smart Resume Screener provides an end-to-end workflow for transforming unstructured PDF resumes into structured candidate profiles and evaluating them against recruiter-defined requirements.



The platform combines:



Resume Parsing

&#x20;     +

Structured Candidate Profiles

&#x20;     +

Multi-Factor Matching

&#x20;     +

Optional Semantic LLM Analysis

&#x20;     +

Candidate Ranking

&#x20;     +

Automated Shortlisting



This creates a practical screening workflow that can help recruiters quickly identify candidates who best satisfy a given job specification.

🎥 Demo Video

Watch the Smart Resume Screener Demo
https://drive.google.com/file/d/1RCDG3GwiXK6wWld_q4aMI2sU4qnoyxRb/view?usp=sharing

