# TrustQuiz - AI-Powered Exam Question Generator

Generate trustworthy practice exam questions from your course materials with full source transparency.

## 🎯 Overview

TrustQuiz addresses a critical problem in AI-assisted learning: trust. While tools like ChatGPT can generate practice questions, students cannot verify their accuracy against actual course materials. TrustQuiz solves this by:

- Generating questions **exclusively from your uploaded PDFs**
- Providing **exact page numbers and source excerpts** for every question
- Testing **application of concepts**, not just memorization
- Auto-detecting **learning objectives** from course materials

Developed as part of the SAI2 (Software Architecture & AI) module at BFH, this project demonstrates practical applications of prompt engineering, RAG (Retrieval-Augmented Generation), and user-centered AI design.

## ✨ Key Features

- **Source Transparency**: Every question includes page number + verifiable excerpt
- **Application-Focused**: Questions test understanding through scenarios, not definitions
- **Learning Objectives Integration**: Auto-detects and aligns with course goals
- **Performance Tracking**: Identifies weak areas and provides study recommendations
- **Clean Interface**: Simple 3-step workflow (Upload → Generate → Practice)

## 🚀 Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/doldm1/sai2-exam-generator.git
cd sai2-exam-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Get an API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create an account (free $5 credits for new users)
3. Generate a new API key
4. Copy it to your `.env` file

**⚠️ Important:** Never commit your `.env` file to Git (already in `.gitignore`)

### 4. Run the App

**On most systems:**
```bash
python -m streamlit run app.py
```

**On Windows (if above doesn't work):**
```bash
py -m streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

## 📖 Usage

1. **Upload Tab**: Upload your course PDF (lecture slides, notes, 15-30 pages)
2. **Generate Tab**: Select number of questions, optionally add learning objectives, click "Start Practice"
3. **Practice Tab**: Answer questions, check answers, view source excerpts for verification

## 🎓 For Students & Educators

**Student Use Cases:**
- Generate practice questions from lecture slides
- Test understanding before exams
- Identify weak areas through performance tracking
- Verify AI-generated content against source material

**Key Differentiator:**
Unlike generic ChatGPT, TrustQuiz provides **verifiable sources** for every question, enabling students to independently confirm accuracy.

## 💰 Cost Estimate

- **Model Used**: GPT-4o (production version, Version 4)
- **Cost**: ~$0.30 for 20-question practice session
- **Billing**: You pay only for what you use through your OpenAI account

## 🏗️ Technical Architecture

### Tech Stack
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4o
- **PDF Processing**: PyMuPDF (fitz)
- **Language**: Python 3.10+

### Prompt Engineering Techniques
- **System Prompting**: Role definition with explicit constraints
- **Few-Shot Learning**: Good vs bad question examples
- **JSON Forcing**: Structured output via `response_format`
- **Context Engineering**: Dynamic learning objectives integration

### Development Iterations
- **Version 1**: Baseline (GPT-4o-mini, basic prompts)
- **Version 2**: Added few-shot learning
- **Version 3**: Anti-memorization rules (quality plateau with GPT-4o-mini)
- **Version 4**: Upgraded to GPT-4o + explicit verification requirements = **Production Ready** ✅

## 📁 Project Structure
```
sai2-exam-generator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # API key template
├── .gitignore               # Git exclusions
├── README.md                # This file
├── utils/
│   ├── prompts.py           # System prompts and prompt generation
│   ├── pdf_parser.py        # PDF text extraction & LO detection
│   ├── question_gen.py      # OpenAI API integration
│   └── analytics.py         # Performance tracking & recommendations
└── storage/
    └── uploads/             # Temporary PDF storage (session-based)
```

## 🔬 Academic Context (SAI2 Module - BFH)

This project demonstrates:
- ✅ **Problem Understanding**: User interviews identified trust as core issue
- ✅ **Solution Design**: Gold standard criteria from student feedback
- ✅ **Prompt Engineering**: Systematic exploration of techniques and models
- ✅ **Evaluation**: Two-phase user testing (3 students V1, 6 students V4)
- ✅ **Iteration**: Evidence-based refinement across 4 major versions
- ✅ **Production Deployment**: Functional prototype solving real user needs

**Key Findings:**
1. Few-shot examples outperform abstract instructions
2. Model capability creates a quality ceiling prompt engineering cannot overcome
3. Explicit verification requirements significantly improve source quality

Full methodology and results documented in accompanying report.

## 🔐 Security & Privacy

- ✅ API keys stored in `.env` (not committed to Git)
- ✅ PDFs processed via OpenAI API (not stored permanently)
- ✅ Session-based operation (no persistent user data)
- ⚠️ Do not upload confidential or sensitive documents

## 📋 Requirements

- Python 3.10 or higher
- OpenAI API key with credits
- Internet connection for API calls
- Text-based PDFs (not scanned images)

## 🛠️ Troubleshooting

### "Python was not found"
**Windows users**: Use `py` instead of `python`:
```bash
py -m streamlit run app.py
```

### "API Key invalid"
- Check your `.env` file exists and contains valid key
- Key should start with `sk-proj-` or `sk-`
- Verify credits at platform.openai.com/usage

### "No text extracted from PDF"
- PDF must be text-based (not scanned images)
- Test: Can you copy/paste text from the PDF?
- Try re-saving PDF or using a different file

### "Module not found"
```bash
pip install -r requirements.txt
```

## 🚢 Deployment

**Local Development:**
Follow Quick Setup above

**Streamlit Cloud (Public Deployment):**
1. Push code to GitHub (ensure `.env` is gitignored!)
2. Go to https://share.streamlit.io/
3. Connect repository and select `app.py`
4. Add OpenAI API key in Streamlit Cloud Secrets:
```toml
   OPENAI_API_KEY = "sk-proj-..."
```
5. Deploy!

**Note**: For public deployment, consider implementing usage limits to prevent API cost abuse.

## 📚 Documentation

- **Full Report**: Detailed methodology, user research, prompt engineering process, and evaluation results
- **Code Repository**: https://github.com/doldm1/sai2-exam-generator
- **Appendices**: Complete prompt text, testing protocols, user feedback analysis

## 👥 Team

- **Marcel Dolder** - Digital Business & AI, BFH
- **Jan Arnet** - Digital Business & AI, BFH  
- **Manuel Eggen** - Digital Business & AI, BFH

Project developed for SAI2 (Software Architecture & AI) module, Fall 2025.

## 📄 License

MIT License - Educational Project

For academic and personal use. Commercial use requires attribution.

## 🙏 Acknowledgments

- BFH SAI2 Module instructors for project guidance
- 6 student testers who provided invaluable feedback
- OpenAI for GPT-4o API access

---

**Version**: 4.0 (Production Ready)  
**Status**: ✅ Deployed and Tested  
**Last Updated**: December 2025