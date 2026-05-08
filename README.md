# Smart Resume Screening System

A Flask web application that ranks candidate resumes against a job description using TF-IDF similarity, with AI-powered resume roasting and optimization via Google Gemini.

## Features

- **Bulk resume upload** — upload multiple PDF resumes at once
- **JD-based matching** — paste any job description and get candidates ranked by relevance score
- **TF-IDF similarity scoring** — cosine similarity between preprocessed resume and JD text
- **Resume viewer** — read extracted resume text in-browser
- **AI resume roast** — Gemini critiques each resume against the JD and suggests fixes
- **AI resume optimizer** — generates a tailored, improved version of the resume (no fabrication)
- **Dark theme UI** with analytics dashboard

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| NLP / ML | scikit-learn (TF-IDF), NLTK, NumPy |
| PDF parsing | PyMuPDF |
| AI features | Google Gemini API (`google-genai`) |
| Deployment | Render (gunicorn), Vercel |

## Getting Started

### Prerequisites

- Python 3.11+
- A free [Google AI Studio](https://aistudio.google.com/app/apikey) API key

### Installation

```bash
git clone https://github.com/akshit-31/smart-resume-screening-system.git
cd smart-resume-screening-system
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_flask_secret_key
DEBUG=False
```

### Run Locally

```bash
python run.py
```

Visit `http://localhost:5000`.

## Usage

1. **Upload resumes** — drag and drop or select PDF files on the home page
2. **Enter a job description** — paste the JD text and click **Match**
3. **View ranked results** — candidates are sorted by match score (0–100)
4. **Roast a resume** — click **Roast** on any result to get AI feedback and a fixed version
5. **Download** — save the roasted/optimized resume as a text file

## Deployment

### Render

A `render.yaml` is included. Connect your GitHub repo to Render, set the env vars (`GEMINI_API_KEY`, `SECRET_KEY`) in the dashboard, and deploy.

### Vercel

A `vercel.json` is included for serverless deployment. Set the same env vars in the Vercel project settings.

## Project Structure

```
├── app.py                  # App entry point
├── run.py                  # Dev server runner
├── backend/
│   ├── config.py           # Flask config (env-driven)
│   ├── routes/
│   │   ├── upload.py       # PDF upload handling
│   │   ├── match.py        # JD input + TF-IDF matching
│   │   ├── results.py      # Ranked results page
│   │   ├── resume_view.py  # In-browser resume reader
│   │   └── roast.py        # AI roast endpoint
│   ├── services/
│   │   ├── parser.py           # PDF text extraction (PyMuPDF)
│   │   ├── preprocessor.py     # NLTK text cleaning
│   │   ├── tfidf_model.py      # TF-IDF vectorization + scoring
│   │   ├── similarity.py       # Cosine similarity util
│   │   ├── ranker.py           # Sort candidates by score
│   │   ├── roast_generator.py  # Gemini roast prompts
│   │   └── ai_resume_generator.py  # Gemini resume optimizer
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS + JS
├── tests/                  # pytest test suite
├── notebooks/              # Model experimentation
└── documents/              # SRS, Jira backlog
```

## Running Tests

```bash
pytest tests/
```

## License

MIT
