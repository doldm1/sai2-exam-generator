# SAI2 Exam Question Generator

AI-powered exam question generator with source transparency for university students.

## 🎯 Features

- Upload PDF course materials
- Generate practice exam questions using AI
- Multiple choice questions with instant feedback
- Source transparency - see which page each question comes from
- Track your accuracy and progress

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
```bash
# Kopiere die Template-Datei
cp .env.example .env

# Editiere .env und füge deinen OpenAI API Key ein
# OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**API Key erhalten:**
1. Gehe zu https://platform.openai.com/api-keys
2. Erstelle einen Account oder logge ein
3. Erstelle einen neuen API Key
4. Kopiere den Key in deine `.env` Datei

### 4. Run the App
```bash
python -m streamlit run app.py
```

Die App öffnet sich automatisch im Browser auf `http://localhost:8501`

## 📖 Usage

1. **Upload Tab**: Upload deine Kurs-PDF (Vorlesungsfolien, Notizen)
2. **Generate Tab**: Klicke "Generate Questions" (dauert 15-30 Sekunden)
3. **Practice Tab**: Beantworte Fragen, überprüfe Antworten, siehe Quellen

## 💰 Costs

- ~$0.01-0.05 pro Session mit GPT-4o-mini
- Sehr günstig für Studenten!

## 🔐 Security

- API Keys werden **NIEMALS** auf Git hochgeladen (`.gitignore`)
- Lokale Verarbeitung, keine Datenspeicherung
- Session-basiert, temporär

## 📋 Requirements

- Python 3.10+
- OpenAI API Key (mit Credits)
- Internetverbindung

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4o-mini
- **PDF Processing**: PyMuPDF
- **Language**: Python

## 📝 Project Structure
```
sai2-exam-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
├── .gitignore            # Git exclusions
├── README.md             # This file
├── utils/
│   ├── prompts.py        # AI prompt templates
│   ├── pdf_parser.py     # PDF text extraction
│   └── question_gen.py   # Question generation logic
└── storage/
    └── uploads/          # Temporary PDF storage
```

## 🎓 For SAI2 Module

Dieses Projekt demonstriert:
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Prompt Engineering
- ✅ Source Transparency
- ✅ Clean Code Architecture
- ✅ Professional Documentation

## ⚠️ Important Notes

- PDFs werden zur Verarbeitung an OpenAI API gesendet
- Keine vertraulichen Dokumente hochladen
- Nur für Lernzwecke, nicht für echte Prüfungen
- Überprüfe immer die Quellen!

## 📞 Troubleshooting

### "API Key invalid"
- Überprüfe `.env` Datei
- Stelle sicher der Key startet mit `sk-`
- Verifiziere Credits auf platform.openai.com

### "No text extracted"
- PDF muss textbasiert sein (keine gescannten Bilder)
- Teste: Kannst du Text im PDF kopieren?

### "Module not found"
- Führe aus: `pip install -r requirements.txt`

## 📄 License

MIT License - Educational Project

## 👤 Author

Marcel - SAI2 Module, BFH

---

**Status**: Week 1 MVP Complete ✅