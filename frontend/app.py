import streamlit as st
import requests


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #1e293b,
            #334155
        );
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.1rem;
        color: #cbd5e1;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .candidate-card {
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        background: white;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
    }

    .candidate-name {
        font-size: 1.3rem;
        font-weight: 700;
    }

    .shortlisted {
        color: #15803d;
        font-weight: 700;
    }

    .rejected {
        color: #dc2626;
        font-weight: 700;
    }

    .skill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        margin: 0.2rem;
        border-radius: 20px;
        background: #e2e8f0;
        font-size: 0.85rem;
    }

    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #64748b;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
    <div class="hero">
        <h1>📄 Smart Resume Screener</h1>
        <p>
            AI-powered resume screening and intelligent
            job matching system.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# JOB DETAILS
# ==================================================

st.markdown(
    '<div class="section-title">💼 Job Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    job_title = st.text_input(
        "Job Title *",
        placeholder="Python Backend Developer"
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

    experience_required = st.text_input(
        "Experience Required",
        placeholder="e.g. 2+ years"
    )

    education_required = st.text_input(
        "Education Required",
        placeholder="e.g. Bachelor's in Computer Science"
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
    placeholder="Describe the role and responsibilities...",
    height=140
)


# ==================================================
# RESUME UPLOAD
# ==================================================

st.markdown(
    '<div class="section-title">📑 Upload Resumes</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} resume(s) ready for screening."
    )

    for file in uploaded_files:

        st.write(
            f"📄 **{file.name}** — "
            f"{file.size / 1024:.1f} KB"
        )


# ==================================================
# SCREEN BUTTON
# ==================================================

st.markdown("")

screen_button = st.button(
    "🔍 Screen Resumes",
    type="primary",
    use_container_width=True
)


# ==================================================
# SCREENING
# ==================================================

if screen_button:

    if not job_title.strip():

        st.error(
            "Please enter the Job Title."
        )

        st.stop()


    if not required_skills.strip():

        st.error(
            "Please enter the Required Skills."
        )

        st.stop()


    if not uploaded_files:

        st.error(
            "Please upload at least one PDF resume."
        )

        st.stop()


    with st.spinner(
        "Analyzing resumes and calculating candidate matches..."
    ):

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
                "experience_required": experience_required,
                "education_required": education_required,
                "job_description": job_description,
                "minimum_score": minimum_score,
            }


            response = requests.post(
                "http://127.0.0.1:8000/screen-multiple",
                files=files,
                data=data,
                timeout=120
            )


            if response.status_code != 200:

                st.error(
                    f"Backend returned HTTP "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )

                st.stop()


            result = response.json()


            if "error" in result:

                st.error(
                    result["error"]
                )

                st.stop()


            st.success(
                "Screening completed successfully!"
            )


            # ======================================
            # SUMMARY
            # ======================================

            st.markdown(
                '<div class="section-title">📊 Screening Summary</div>',
                unsafe_allow_html=True
            )


            total = result.get(
                "total_candidates",
                0
            )

            shortlisted = result.get(
                "shortlisted",
                0
            )

            threshold = result.get(
                "minimum_score",
                0
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Total Candidates",
                    total
                )


            with col2:

                st.metric(
                    "Shortlisted",
                    shortlisted
                )


            with col3:

                st.metric(
                    "Minimum Score",
                    f"{threshold}%"
                )


            # ======================================
            # RESULTS
            # ======================================

            st.markdown(
                '<div class="section-title">🏆 Ranked Candidates</div>',
                unsafe_allow_html=True
            )


            candidates = result.get(
                "candidates",
                []
            )


            for candidate in candidates:

                rank = candidate.get(
                    "rank",
                    0
                )

                name = candidate.get(
                    "name"
                ) or "Unknown Candidate"

                filename = candidate.get(
                    "filename",
                    ""
                )

                score = candidate.get(
                    "score",
                    0
                )

                is_shortlisted = candidate.get(
                    "shortlisted",
                    False
                )


                if is_shortlisted:

                    status = "✅ SHORTLISTED"

                    status_class = "shortlisted"

                else:

                    status = "❌ NOT SHORTLISTED"

                    status_class = "rejected"


                # ----------------------------------
                # Candidate header
                # ----------------------------------

                # Use Streamlit's native components for the candidate
                # header instead of raw HTML so the tags can never be
                # displayed as plain text.
                st.markdown(
                    f"### #{rank} — {name}"
                )

                st.write(
                    f"📄 {filename}"
                )

                if is_shortlisted:
                    st.success(status)
                else:
                    st.error(status)


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Match Score",
                        f"{score}%"
                    )


                with col2:

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


                # ----------------------------------
                # Skills
                # ----------------------------------

                if matched:

                    st.write(
                        "**✅ Matched Skills**"
                    )

                    st.write(
                        " • ".join(matched)
                    )

                if missing:

                    st.write(
                        "**❌ Missing Skills**"
                    )

                    st.write(
                        " • ".join(missing)
                    )

                preferred_matched = candidate.get(
                    "preferred_matched_skills",
                    []
                )

                preferred_missing = candidate.get(
                    "preferred_missing_skills",
                    []
                )

                if preferred_matched:
                    st.write(
                        "**⭐ Preferred Skills Matched:**",
                        ", ".join(preferred_matched)
                    )

                if preferred_missing:
                    st.write(
                        "**⚪ Preferred Skills Missing:**",
                        ", ".join(preferred_missing)
                    )

                experience_score = candidate.get(
                    "experience_score",
                    0.0
                )

                education_score = candidate.get(
                    "education_score",
                    0.0
                )

                experience_match = candidate.get(
                    "experience_match"
                )

                education_match = candidate.get(
                    "education_match"
                )

                if experience_match:
                    st.write(
                        "**💼 Experience Match**"
                    )

                    st.write(
                        f"{experience_score}% — {experience_match}"
                    )

                if education_match:
                    st.write(
                        "**🎓 Education Match**"
                    )

                    st.write(
                        f"{education_score}% — {education_match}"
                    )

                description_score = candidate.get(
                    "description_score",
                    0.0
                )

                description_match = candidate.get(
                    "description_match"
                )

                if description_match:
                    st.write(
                        "**📝 Job Description Match**"
                    )

                    st.write(
                        f"{description_score}% — {description_match}"
                    )

                
                # ----------------------------------
                # Details
                # ----------------------------------

                with st.expander(
                    "View Candidate Details"
                ):

                    strengths = candidate.get(
                        "strengths",
                        []
                    )

                    concerns = candidate.get(
                        "concerns",
                        []
                    )

                    justification = candidate.get(
                        "justification"
                    )


                    if strengths:

                        st.write(
                            "### 💪 Strengths"
                        )

                        for item in strengths:

                            st.write(
                                f"• {item}"
                            )


                    if concerns:

                        st.write(
                            "### ⚠️ Concerns"
                        )

                        for item in concerns:

                            st.write(
                                f"• {item}"
                            )


                    if justification:

                        st.write(
                            "### 📝 Justification"
                        )

                        st.write(
                            justification
                        )


                st.divider()


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.info(
                "Make sure this is running in another terminal:"
            )

            st.code(
                "uvicorn backend.api:app --reload"
            )


        except requests.exceptions.Timeout:

            st.error(
                "The screening request timed out."
            )


        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        Smart Resume Screener • AI-powered candidate matching
    </div>
    """,
    unsafe_allow_html=True
)