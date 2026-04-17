# Smart Resume Screener 🎯

An AI-powered resume screening web app built with Flask. Upload multiple PDF resumes, enter a job description, and get ranked candidates using TF-IDF and optional BERT semantic matching.

---

## Features

- 📄 Upload multiple PDF resumes
- 🔍 TF-IDF based keyword matching (fast)
- 🤖 BERT semantic matching (accurate, optional)
- 📊 Ranked results with match scores
- 🚀 Deploy-ready on Render

---

## Project Structure

```
smart-resume-screening/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── routes/              # Upload, Match, Results routes
│   ├── services/            # NLP services (parser, TF-IDF, BERT, ranker)
│   ├── models/              # Data models
│   ├── static/              # CSS, JS, uploaded files
│   └── templates/           # HTML templates
├── tests/                   # Unit tests
├── notebooks/               # Model experiments
├── run.py                   # Entry point
├── requirements.txt
├── Procfile
└── .env
```

---

## Setup & Run Locally

### 1. Clone & create virtual environment
```bash
git clone <your-repo-url>
cd smart-resume-screening
python -m venv venv
```

### 2. Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
# Edit .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run the app
```bash
python run.py
```

Visit `http://127.0.0.1:5000`

---

## Enable BERT (Optional)

Uncomment in `requirements.txt` and install:
```bash
pip install sentence-transformers torch
```

Then toggle "Use BERT" on the matching page.

---

## Deploy on Render

1. Push code to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn run:app`
5. Add environment variable: `SECRET_KEY=your-secret`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| PDF Parsing | PyMuPDF |
| NLP | NLTK, scikit-learn |
| Semantic AI | BERT (sentence-transformers) |
| Frontend | Bootstrap 5 |
| Deployment | Render + Gunicorn |

---

Built by **Akshit** · 4 Weeks · 61 Story Points
