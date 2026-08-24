import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resume_screener.db"
)


def get_connection():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT,
            experience TEXT,
            projects TEXT,
            certifications TEXT,
            achievements TEXT,
            summary TEXT,
            created_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_candidate(candidate):
    connection = get_connection()

    education = [
        education.model_dump()
        for education in candidate.education
    ]

    experience = [
        experience.model_dump()
        for experience in candidate.experience
    ]

    projects = [
        project.model_dump()
        for project in candidate.projects
    ]

    connection.execute(
        """
        INSERT INTO candidates (
            candidate_name,
            email,
            phone,
            skills,
            education,
            experience,
            projects,
            certifications,
            achievements,
            summary,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            candidate.name,
            candidate.email,
            candidate.phone,
            str(candidate.skills),
            str(education),
            str(experience),
            str(projects),
            str(candidate.certifications),
            str(candidate.achievements),
            candidate.summary,
            datetime.now().isoformat(),
        ),
    )

    connection.commit()
    connection.close()