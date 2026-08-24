import streamlit as st
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📄 Smart Resume Screener")

st.write(
    "AI-powered resume screening and job matching system"
)

st.divider()


# --------------------------------------------------
# JOB DETAILS
# --------------------------------------------------

st.header("💼 Job Details")

col1, col2 = st.columns(2)

with col1:

    job_title = st.text_input(
        "Job Title *",
        placeholder="Example: Python Backend Developer"
    )

    required_skills = st.text_input(
        "Required Skills *",
        placeholder="Python, FastAPI, SQL, Docker"
    )

with col2:

    preferred_skills = st.text_input(
        "Preferred Skills",
        placeholder="AWS, Git, Linux"
    )

    minimum_score = st.number_input(
        "Minimum Score",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=5.0
    )

job_description = st.text_area(
    "Job Description",
    placeholder="Enter the job description here...",
    height=150
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.header("📑 Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} resume(s) uploaded"
    )

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )


st.divider()


# --------------------------------------------------
# SCREEN BUTTON
# --------------------------------------------------

screen_button = st.button(
    "🔍 Screen Resumes",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# SCREENING
# --------------------------------------------------

if screen_button:

    if not job_title.strip():

        st.error(
            "Please enter the Job Title."
        )

    elif not required_skills.strip():

        st.error(
            "Please enter the Required Skills."
        )

    elif not uploaded_files:

        st.error(
            "Please upload at least one PDF resume."
        )

    else:

        st.info(
            "Screening resumes..."
        )

        try:

            files = []

            for file in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf"
                        )
                    )
                )

            data = {

                "job_title": job_title,

                "required_skills": required_skills,

                "preferred_skills": preferred_skills,

                "job_description": job_description,

                "minimum_score": str(
                    minimum_score
                )
            }

            response = requests.post(
                "http://127.0.0.1:8000/screen-multiple",
                files=files,
                data=data,
                timeout=120
            )


            # --------------------------------------
            # RESPONSE HANDLING
            # --------------------------------------

            if response.status_code == 200:

                result = response.json()

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        "Screening completed successfully!"
                    )


                    # ----------------------------------
                    # SUMMARY
                    # ----------------------------------

                    st.header("📊 Screening Summary")

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Total Candidates",
                            result.get(
                                "total_candidates",
                                0
                            )
                        )

                    with col2:

                        st.metric(
                            "Shortlisted",
                            result.get(
                                "shortlisted",
                                0
                            )
                        )

                    with col3:

                        st.metric(
                            "Minimum Score",
                            f"{result.get('minimum_score', 0)}%"
                        )


                    # ----------------------------------
                    # CANDIDATE RESULTS
                    # ----------------------------------

                    st.header(
                        "🏆 Ranked Candidates"
                    )

                    candidates = result.get(
                        "candidates",
                        []
                    )


                    for candidate in candidates:

                        score = candidate.get(
                            "score",
                            0
                        )

                        shortlisted = candidate.get(
                            "shortlisted",
                            False
                        )


                        if shortlisted:

                            status = "✅ SHORTLISTED"

                        else:

                            status = "❌ NOT SHORTLISTED"


                        with st.container():

                            st.subheader(
                                f"#{candidate.get('rank')} "
                                f"— "
                                f"{candidate.get('name') or 'Unknown Candidate'}"
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:

                                st.metric(
                                    "Match Score",
                                    f"{score}%"
                                )

                            with col2:

                                st.write(
                                    "**Status**"
                                )

                                st.write(
                                    status
                                )

                            with col3:

                                st.write(
                                    "**Resume**"
                                )

                                st.write(
                                    candidate.get(
                                        "filename",
                                        ""
                                    )
                                )


                            st.progress(
                                min(
                                    max(
                                        score / 100,
                                        0.0
                                    ),
                                    1.0
                                )
                            )


                            matched = candidate.get(
                                "matched_skills",
                                []
                            )

                            missing = candidate.get(
                                "missing_skills",
                                []
                            )


                            if matched:

                                st.write(
                                    "**Matched Skills:** "
                                    + ", ".join(matched)
                                )

                            if missing:

                                st.write(
                                    "**Missing Skills:** "
                                    + ", ".join(missing)
                                )


                            strengths = candidate.get(
                                "strengths",
                                []
                            )

                            concerns = candidate.get(
                                "concerns",
                                []
                            )


                            if strengths:

                                with st.expander(
                                    "💪 Strengths"
                                ):

                                    for strength in strengths:

                                        st.write(
                                            f"• {strength}"
                                        )


                            if concerns:

                                with st.expander(
                                    "⚠️ Concerns"
                                ):

                                    for concern in concerns:

                                        st.write(
                                            f"• {concern}"
                                        )


                            justification = candidate.get(
                                "justification"
                            )

                            if justification:

                                st.write(
                                    "**Justification:** "
                                    + justification
                                )


                            st.divider()


            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.code(
                    response.text
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The screening request timed out."
            )


        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )