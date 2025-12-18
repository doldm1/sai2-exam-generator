"""
SAI2 Exam Question Generator - Main Streamlit Application

A tool for generating exam questions from course materials with source transparency.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
import json

from utils.pdf_parser import extract_text_from_pdf, get_pdf_metadata, extract_learning_objectives
from utils.question_gen import generate_questions, grade_answer, check_api_key
from utils.analytics import display_performance_summary, get_study_recommendation, calculate_performance_stats

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TrustQuiz",
    page_icon="📚",
    layout="wide",
)

# Custom CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Main title styling */
    h1 {
        color: #1a1a1a;
        font-size: 2.8em;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2em;
        padding: 12px 24px;
        font-weight: 500;
    }
    
    /* Header styling */
    h2 {
        color: #2c2c2c;
        font-size: 1.8em;
        margin-top: 20px;
        font-weight: 600;
    }
    
    h3 {
        color: #e67e22;
        font-size: 1.5em;
        font-weight: 600;
    }
    
    h4 {
        color: #333;
        font-size: 1.3em;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #e67e22;
        color: white;
        font-size: 1.1em;
        padding: 12px 24px;
        border-radius: 6px;
        border: none;
        font-weight: 600;
        font-family: 'Roboto', sans-serif !important;
    }
    
    .stButton > button:hover {
        background-color: #d35400;
        color: white !important;
    }
    
    /* Info/warning/error boxes */
    .stAlert {
        font-size: 1.05em;
        padding: 15px;
    }
    
    /* Text area and input */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 1.1em;
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    
    .stMetric > div:first-child {
        font-size: 1.3em;
        color: #333;
        font-weight: 500;
    }
    
    .stMetric > div:last-child {
        font-size: 1.8em;
        color: #e67e22;
        font-weight: 700;
    }

    /* Hide the top stripe/header */
    .stAppHeader {
        display: none;
    }

    /* Alternative: hide just the decoration line */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Remove top padding */
    .appview-container {
        padding-top: 0 !important;
    }

    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        h1 {
            color: #ffffff !important;
        }
        
        h2 {
            color: #e8e8e8 !important;
        }
        
        h4 {
            color: #e8e8e8 !important;
        }

        .stMetric > div:first-child {
            color: #e8e8e8 !important;
        }

        .stMetric {
            background-color: #2b2b2b !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None
if 'pdf_metadata' not in st.session_state:
    st.session_state.pdf_metadata = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')
if 'detected_objectives' not in st.session_state:
    st.session_state.detected_objectives = None
if 'prefilled_objectives' not in st.session_state:
    st.session_state.prefilled_objectives = ''


def main():
    """Main application function."""
    
    st.title("TrustQuiz")
    st.markdown("<p style='font-size: 1.2em; color: #555;'>Generate practice exam questions from your course materials with full source transparency.</p>", unsafe_allow_html=True)
    
    # Info banner
    st.info("""
        📚 **Welcome to TrustQuiz** - Generate trustworthy practice questions from your course materials.
        
        ⚠️ **Privacy Notice**: PDFs are processed via OpenAI API. Do not upload confidential documents.
    """)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
        )
        st.session_state.api_key = api_key
        
        if api_key:
            if check_api_key(api_key):
                st.success("✅ API Key valid")
            else:
                st.error("❌ API Key invalid")
        else:
            st.info("👆 Enter your OpenAI API key to get started")
            st.caption("Get one at: platform.openai.com/api-keys")
            st.caption("💰 Cost: ~$0.30 for 20 questions")
        
        
        st.divider()
        
        # Stats
        if st.session_state.pdf_content:
            st.subheader("Document Info")
            if st.session_state.pdf_metadata:
                st.write(f"**Pages:** {st.session_state.pdf_metadata.get('pages', 'N/A')}")
                st.write(f"**Title:** {st.session_state.pdf_metadata.get('title', 'Unknown')}")
        
        if st.session_state.questions:
            st.subheader("Progress")
            answered = len(st.session_state.user_answers)
            total = len(st.session_state.questions)
            st.progress(answered / total if total > 0 else 0)
            st.write(f"{answered}/{total} answered")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["Upload", "Generate", "Practice"])
    
    with tab1:
        upload_tab()
    
    with tab2:
        generate_tab(5, None)  # Default values, actual values set in the tab
    
    with tab3:
        practice_tab()


def upload_tab():
    st.header("Upload Your Study Material")
    st.write("Upload your lecture slides, notes, or course PDFs to generate personalized practice questions.")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload lecture slides, notes, or study materials in PDF format"
    )
    
    if uploaded_file is not None:
        # Save the file temporarily
        upload_dir = Path("storage/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Uploaded: {uploaded_file.name}")
        
        # Parse the PDF
        with st.spinner("Extracting text from PDF..."):
            try:
                pages_content, total_pages = extract_text_from_pdf(str(file_path))
                metadata = get_pdf_metadata(str(file_path))
                
                st.session_state.pdf_content = pages_content
                st.session_state.pdf_metadata = metadata
                
                # Auto-detect learning objectives
                detected = extract_learning_objectives(pages_content)
                st.session_state.detected_objectives = detected
                
                st.success(f"Material loaded! Found {total_pages} pages. Ready to generate questions.")
                
                if detected:
                    st.success(f"Automatically detected {len(detected)} learning objectives!")
                
                # Show preview
                with st.expander("Preview extracted content"):
                    preview_pages = min(3, total_pages)
                    for i in range(1, preview_pages + 1):
                        st.subheader(f"Page {i}")
                        st.text(pages_content[i][:500] + "..." if len(pages_content[i]) > 500 else pages_content[i])
                
            except Exception as e:
                st.error(f"Error parsing PDF: {str(e)}")
    
    elif st.session_state.pdf_content:
        st.success(f"Document loaded: {st.session_state.pdf_metadata.get('pages', 'N/A')} pages")
        
        # Add button to proceed
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Generate Questions", type="primary", use_container_width=True):
                # Switch to generate tab
                st.rerun()


def generate_tab(num_questions, topic_filter):
    """Generate exam questions from uploaded content."""
    st.header("Start Practice Session")
    
    if not st.session_state.pdf_content:
        st.warning("Please upload a PDF file first in the Upload tab.")
        return
    
    if not st.session_state.api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return
    
    # Number of questions selector (moved from sidebar)
    num_questions = st.slider(
        "How many questions do you want to practice?",
        min_value=1,
        max_value=20,
        value=5,
        help="Select the number of practice questions to generate"
    )
    
    if not st.session_state.pdf_content:
        st.warning("Please upload a PDF file first in the Upload tab.")
        return
    
    if not st.session_state.api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return
    
    st.markdown("<p style='font-size: 1.1em;'>Generate personalized practice questions to test your understanding of the material.</p>", unsafe_allow_html=True)
    
    # Show detected objectives if found
    if st.session_state.detected_objectives:
        with st.expander("Detected learning objectives (auto-detected)", expanded=False):
            st.info("The tool found these potential learning objectives in the PDF:")
            for obj in st.session_state.detected_objectives:
                st.markdown(f"- {obj}")
            
            if st.button("Use detected objectives"):
                st.session_state.prefilled_objectives = "\n".join(f"- {obj}" for obj in st.session_state.detected_objectives)
                st.rerun()
    
    # Lernziele Eingabe (optional)
    st.subheader("Learning Objectives (optional)")
    
    # Pre-fill if user clicked button
    default_value = st.session_state.prefilled_objectives
    
    learning_objectives = st.text_area(
        "Which learning objectives should the questions cover?",
        value=default_value,
        placeholder="e.g.:\n- Understand concept X\n- Apply method Y\n- Analyze problem Z\n\nOr leave blank for general questions from the material.",
        height=120,
        help="Optional: Enter learning objectives or use the auto-detected ones. Leave empty for general questions."
    )
    
    st.divider()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(f"Document ready: {st.session_state.pdf_metadata.get('pages', 'N/A')} pages")
    
    with col2:
        if st.button("Start Practice", type="primary", use_container_width=True):
            generate_questions_action(num_questions, topic_filter if topic_filter else None, learning_objectives)
    
    # Show existing questions if any
    if st.session_state.questions:
        st.success(f"{len(st.session_state.questions)} questions generated")
        
        with st.expander("Preview generated questions"):
            for idx, q in enumerate(st.session_state.questions, 1):
                st.markdown(f"**Q{idx}:** {q['question']}")
                st.caption(f"Source: Page {q['source_page']}")
                st.divider()


def generate_questions_action(num_questions, topic_filter, learning_objectives=None):
    """Action to generate questions using the LLM."""
    with st.spinner("Generating questions... This may take 15-30 seconds..."):
        try:
            # Store learning objectives in session state for later reference
            if learning_objectives:
                st.session_state.learning_objectives = learning_objectives
            
            questions = generate_questions(
                pages_content=st.session_state.pdf_content,
                api_key=st.session_state.api_key,
                num_questions=num_questions,
                topic=topic_filter if topic_filter else None,
                learning_objectives=learning_objectives if learning_objectives else None,
                temperature=0.3
            )
            
            st.session_state.questions = questions
            st.session_state.current_question_idx = 0
            st.session_state.user_answers = {}
            st.session_state.show_feedback = {}
            
            st.success(f"Your practice session is ready! {len(questions)} questions generated!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")


def practice_tab():
    """Practice with generated questions."""
    st.header("Check Your Knowledge")
    
    if not st.session_state.questions:
        st.warning("Please generate questions first in the Generate tab.")
        return
    
    questions = st.session_state.questions
    total_questions = len(questions)
    
    # Question navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("Previous") and st.session_state.current_question_idx > 0:
            st.session_state.current_question_idx -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"<h4 style='text-align: center;'>Question {st.session_state.current_question_idx + 1} of {total_questions}</h4>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next") and st.session_state.current_question_idx < total_questions - 1:
            st.session_state.current_question_idx += 1
            st.rerun()
    
    st.divider()
    
    # Display current question
    current_q = questions[st.session_state.current_question_idx]
    q_id = st.session_state.current_question_idx
    
    st.markdown(f"<h3 style='color: #1a1a1a; font-size: 1.6em;'>{current_q['question']}</h3>", unsafe_allow_html=True)
    
    # Answer options
    user_answer = st.radio(
        "Select your answer:",
        options=current_q['options'],
        key=f"question_{q_id}",
        index=None
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Check Answer", type="primary", disabled=user_answer is None):
            if user_answer:
                result = grade_answer(
                    question=current_q['question'],
                    correct_answer=current_q['correct_answer'],
                    user_answer=user_answer,
                    explanation=current_q['explanation'],
                    api_key=st.session_state.api_key
                )
                
                st.session_state.user_answers[q_id] = {
                    'answer': user_answer,
                    'is_correct': result['is_correct'],
                    'feedback': result['feedback']
                }
                st.session_state.show_feedback[q_id] = True
                st.rerun()
    
    with col2:
        if st.button("Show Source"):
            show_source_modal(current_q)
    
    # Show feedback if answer has been checked
    if q_id in st.session_state.show_feedback and st.session_state.show_feedback[q_id]:
        result = st.session_state.user_answers[q_id]
        
        if result['is_correct']:
            st.success(f"{result['feedback']}")
        else:
            st.error(f"{result['feedback']}")
    
    # Progress summary at bottom
    st.divider()
    display_summary()


def show_source_modal(question):
    """Display source information for a question."""
    # Beautiful card-style source display
    with st.container():
        st.markdown("""
        <style>
        .source-card {
            background-color: #f5f5f5;
            border-left: 4px solid #e67e22;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .source-page {
            color: #1a1a1a;
            font-weight: bold;
            font-size: 1.1em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="source-card">
            <h4 style='margin-top: 0; color: #2c3e50;'>Source Reference</h4>
            <p><span class="source-page">Page: {question['source_page']}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        if 'source_excerpt' in question and question['source_excerpt']:
            st.markdown("**Source Excerpt:**")
            st.info(question['source_excerpt'])
    
    # Show full page content
    if st.session_state.pdf_content and question['source_page'] in st.session_state.pdf_content:
        with st.expander("View full page content"):
            page_text = st.session_state.pdf_content[question['source_page']]
            st.text_area(
                f"Page {question['source_page']} content:",
                value=page_text,
                height=300,
                disabled=True,
                key=f"source_page_{question['source_page']}_{hash(question['question'])}"  # Unique key!
            )


def display_summary():
    """Display summary of answers with performance analysis."""
    if not st.session_state.user_answers:
        return
    
    total = len(st.session_state.questions)
    answered = len(st.session_state.user_answers)
    correct = sum(1 for ans in st.session_state.user_answers.values() if ans['is_correct'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Answered", f"{answered}/{total}")
    
    with col2:
        st.metric("Correct", f"{correct}/{answered}" if answered > 0 else "0/0")
    
    with col3:
        accuracy = (correct / answered * 100) if answered > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    # Add performance summary if all questions answered
    if answered == total:
        st.markdown("---")
        
        # Build results list for analytics
        results = []
        for q_id, answer_data in st.session_state.user_answers.items():
            question = st.session_state.questions[q_id]
            results.append({
                'question': question['question'],
                'is_correct': answer_data['is_correct']
            })
        
        # Display performance summary
        display_performance_summary(results)
        
        # Study recommendation
        stats = calculate_performance_stats(results)
        recommendation = get_study_recommendation(stats['percentage'])
        
        st.markdown("### Next Steps")
        st.info(recommendation)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate More Questions", use_container_width=True):
                # Reset for new practice session
                st.session_state.questions = []
                st.session_state.user_answers = {}
                st.session_state.show_feedback = {}
                st.session_state.current_question_idx = 0
                st.rerun()
        with col2:
            if st.button("Review Source Material", use_container_width=True):
                st.info("Tip: Re-read the sections related to your weak areas in the original PDF!")


if __name__ == "__main__":
    main()