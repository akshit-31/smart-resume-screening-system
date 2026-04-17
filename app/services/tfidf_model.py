from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_tfidf_similarity(jd_text: str, resume_text: str) -> float:
    """
    Compute cosine similarity between job description and resume using TF-IDF vectors.
    Returns a score between 0 and 1.
    """
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(score)
    except Exception as e:
        raise ValueError(f"TF-IDF similarity failed: {str(e)}")
