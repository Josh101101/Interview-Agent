import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel, Field
from typing import Union, List, Optional
from dotenv import load_dotenv
import os
import json
from PyPDF2 import PdfReader
from docx import Document
import ast
from utils import extract_text_from_pdf, extract_text_from_docx, get_resume_text, extract_json_from_output

# Load environment variables
load_dotenv()

# LLM Initialization
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=1.0
)

# Candidate profile model
class CandidateProfile(BaseModel):
    name: str = Field(description="Candidate's full name")
    email: str = Field(description="Candidate's email address")
    experience: Union[str, List] = Field(description="experience")
    projects: Union[str, List] = Field(description="projects")
    education: Union[str, List] = Field(description="education")
    skills: Union[str, List] = Field(description="skills")
    extracurricular: Union[str, List] = Field(description="extracurricular")
    achievements: Optional[Union[str, List]] = Field(description="achievements")
    certifications: Optional[Union[str, List]] = Field(description="certifications")
    resume: str = Field(description="Resume text or summary")

def sidebar_inputs():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=60)
        st.markdown("# <span style='color:#235390'>AI Interview Agent</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 1️⃣ Upload Your Resume")
        uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
        resume_text = ""
        if uploaded_file:
            filetype = uploaded_file.type
            if filetype == "application/pdf":
                resume_text = get_resume_text(uploaded_file, "pdf")
            elif filetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = get_resume_text(uploaded_file, "docx")
            else:
                resume_text = get_resume_text(uploaded_file, "text")
            st.markdown("### 📄 Resume Text Preview")
            st.text_area("Resume Text", resume_text, height=150, key="sidebar_resume_text")
        st.markdown("---")
        st.markdown("### 📝 Job Details")
        job_position = st.text_input("Job Position", value="Data Scientist", key="sidebar_job_position")
        job_description = st.text_area("Job Description", value="We are seeking a Data Scientist with strong experience in Python, machine learning, and data analysis. The candidate should be able to build predictive models, work with large datasets, and communicate insights effectively.", key="sidebar_job_desc")
        num_questions = st.slider("Number of Questions", min_value=1, max_value=30, value=5, key="sidebar_num_questions")
        st.markdown("---")
    return uploaded_file, resume_text, job_position, job_description, num_questions

# Step 2: Parse Resume

def parse_resume_section(resume_text, llm):
    st.subheader("Parsed Candidate Profile")
    resume_parser_agent = Agent(
        role="Resume Parser",
        goal="Extract structured candidate information from resume text",
        backstory="You are an expert at reading resumes and extracting key candidate details for interview preparation.",
        llm=llm
    )
    parse_resume_task = Task(
        description=(
            "Parse the following resume and extract name, email, experience, projects, education, skills, extracurricular, achievements, certifications as JSON:\n"
            + resume_text
        ),
        agent=resume_parser_agent,
        expected_output="A JSON object with keys: name, email, experience, projects, education, skills, extracurricular, achievements, certifications."
    )
    crew = Crew(agents=[resume_parser_agent], tasks=[parse_resume_task])
    with st.spinner("Parsing resume..."):
        try:
            results = crew.kickoff()
        except Exception as e:
            st.error(f"Error running resume parser agent: {e}")
            st.stop()
    import re
    try:
        results_json = extract_json_from_output(results)
        results_json = re.sub(r'^```[a-zA-Z]*\n', '', results_json.strip())
        results_json = re.sub(r'```$', '', results_json.strip())
        try:
            profile = json.loads(results_json)
        except Exception:
            try:
                profile = ast.literal_eval(results_json)
            except Exception:
                fixed = re.sub(r"'", '"', results_json)
                profile = json.loads(fixed)
        return profile
    except Exception as e:
        st.error(f"Error parsing profile: {e}\nRaw output: {results_json if 'results_json' in locals() else results}")
        st.stop()

def generate_questions_section(profile, job_position, job_description, num_questions, llm):
    st.subheader("📝 Generate Interview Questions")
    st.markdown(
        "<span style='color:#235390'>Click below to get tailored questions:</span>",
        unsafe_allow_html=True
    )
    if st.button("✨ Generate Questions", use_container_width=True):
        batch_size = 10  # Number of questions per batch
        questions = []
        import re
        import time
        for start in range(0, num_questions, batch_size):
            this_batch = min(batch_size, num_questions - start)
            question_agent = Agent(
                role="Interview Question Generator",
                goal="Generate technical, behavioral, situational interview questions based on candidate profile and job description",
                backstory="You are an expert interviewer who creates relevant questions for candidates based on the job they are applying for.",
                llm=llm
            )
            question_task = Task(
                description=(
                    f"You are preparing for an interview for the position of '{job_position}'.\n"
                    f"Job Description: {job_description}\n"
                    f"Based on the following candidate profile, generate {this_batch} technical interview questions relevant to their experience, skills, and projects, and the job description above. The goal is to assess the candidate's skills, experience, and suitability for the role. "
                    "Return ONLY a JSON list of objects with the key 'question'.\n"
                    f"Candidate Profile:\n{json.dumps(profile)}"
                ),
                agent=question_agent,
                expected_output="A JSON list of objects with the key 'question'."
            )
            crew = Crew(agents=[question_agent], tasks=[question_task])
            with st.spinner(f"Generating questions {start+1}-{start+this_batch}..."):
                try:
                    questions_output = crew.kickoff()
                except Exception as e:
                    st.error(f"Error running question generator agent: {e}")
                    st.stop()
            try:
                questions_json = extract_json_from_output(questions_output)
                questions_json = re.sub(r'^```[a-zA-Z]*\n', '', questions_json.strip())
                questions_json = re.sub(r'```$', '', questions_json.strip())
                match = re.search(r'\[.*\]', questions_json, re.DOTALL)
                if match:
                    questions_json = match.group(0)
                try:
                    batch_questions = json.loads(questions_json)
                except Exception:
                    try:
                        batch_questions = ast.literal_eval(questions_json)
                    except Exception:
                        fixed = questions_json.replace("'", '"')
                        batch_questions = json.loads(fixed)
                questions.extend(batch_questions)
            except Exception as e:
                st.error(f"Error parsing questions: {e}\nRaw output: {questions_json if 'questions_json' in locals() else questions_output}")
                st.stop()
            time.sleep(1)  # Optional: avoid rate limits
        st.session_state["questions"] = questions
        st.session_state["answers"] = ["" for _ in questions]
        st.success("Questions generated!")

def answer_questions_section():
    if "questions" in st.session_state:
        st.subheader("💬 Answer the Questions")
        st.markdown("<span style='color:#235390'>Type or paste your answers below:</span>", unsafe_allow_html=True)
        answers = []
        for idx, q in enumerate(st.session_state["questions"]):
            with st.expander(f"Q{idx+1}: {q['question']}"):
                answer = st.text_area("Your Answer", value=st.session_state["answers"][idx], key=f"answer_{idx}")
                answers.append({"question": q["question"], "answer": answer})
        st.session_state["answers"] = [a["answer"] for a in answers]
        st.markdown("---")
        return answers
    return []

def evaluate_answers_section(answers, llm):
    if st.button("🚀 Evaluate Answers", use_container_width=True):
        evaluation_agent = Agent(
            role="Answer Evaluation Agent",
            goal="Evaluate candidate answers and provide feedback using LLM",
            backstory="You are an expert technical interviewer who scores and comments on candidate answers.",
            llm=llm
        )
        feedback_task = Task(
            description=(
                "You are an expert technical interviewer. For each question and answer pair below, provide a score (0-10) and a short feedback comment. "
                "Return ONLY a JSON list of objects with keys: question, answer, score, comments.\n"
                f"Q&A Pairs: {json.dumps(answers, ensure_ascii=False)}"
            ),
            agent=evaluation_agent,
            expected_output="A JSON list of objects with keys: question, answer, score, comments."
        )
        crew = Crew(agents=[evaluation_agent], tasks=[feedback_task])
        with st.spinner("Evaluating answers..."):
            try:
                feedback_output = crew.kickoff()
            except Exception as e:
                st.error(f"Error running evaluation agent: {e}")
                st.stop()
        import re
        try:
            feedback_json = extract_json_from_output(feedback_output)
            feedback_json = re.sub(r'^```[a-zA-Z]*\n', '', feedback_json.strip())
            feedback_json = re.sub(r'```$', '', feedback_json.strip())
            match = re.search(r'\[.*\]', feedback_json, re.DOTALL)
            if match:
                feedback_json = match.group(0)
            try:
                feedback = json.loads(feedback_json)
            except Exception:
                try:
                    feedback = ast.literal_eval(feedback_json)
                except Exception:
                    fixed = feedback_json.replace("'", '"')
                    feedback = json.loads(fixed)
            st.subheader("Feedback Results")
            for f in feedback:
                st.markdown(f"**Q:** {f.get('question', '')}")
                st.markdown(f"**A:** {f.get('answer', '')}")
                st.markdown(f"**Score:** {f.get('score', '')}")
                st.markdown(f"**Comments:** {f.get('comments', '')}")
                st.markdown("---")
            # Add download button for CSV
            import io
            import csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Question", "Answer", "Score", "Comments"])
            for f in feedback:
                writer.writerow([
                    f.get('question', ''),
                    f.get('answer', ''),
                    f.get('score', ''),
                    f.get('comments', '')
                ])
            st.download_button(
                label="Download Q&A and Feedback as CSV",
                data=output.getvalue(),
                file_name="interview_results.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error parsing feedback: {e}\nRaw output: {feedback_json if 'feedback_json' in locals() else feedback_output}")
            st.stop()

def main():
    st.set_page_config(
        page_title="AI Interview Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(
        """
        <style>
        .main {
            background-color: #f7f9fa;
        }
        .stButton>button {
            border-radius: 8px;
            background: linear-gradient(90deg, #4f8bf9 0%, #235390 100%);
            color: white;
            font-weight: 600;
            padding: 0.5em 2em;
            margin: 0.5em 0;
        }
        .stTextArea textarea {
            border-radius: 8px;
            min-height: 100px;
        }
        .stFileUploader>div>div {
            border-radius: 8px;
            border: 2px dashed #4f8bf9;
            background: #eaf1fb;
        }
        .stSubheader, .stMarkdown h2 {
            color: #235390;
        }
        .stExpanderHeader {
            font-weight: bold;
            color: #235390;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    uploaded_file, resume_text, job_position, job_description, num_questions = sidebar_inputs()
    if uploaded_file:
        st.markdown("---")
        profile = parse_resume_section(resume_text, llm)
        generate_questions_section(profile, job_position, job_description, num_questions, llm)
        answers = answer_questions_section()
        evaluate_answers_section(answers, llm)

if __name__ == "__main__":
    main()
