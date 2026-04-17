import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.preprocessor import preprocess_text
from app.services.tfidf_model import compute_tfidf_similarity
from app.services.ranker import rank_candidates


def test_preprocess_text_basic():
    text = "Hello World! This is a TEST sentence with 123 numbers."
    result = preprocess_text(text)
    assert isinstance(result, str)
    assert '123' not in result
    assert 'Hello' not in result  # should be lowercased or removed


def test_preprocess_text_empty():
    assert preprocess_text("") == ""


def test_tfidf_similarity_identical():
    text = "python developer flask rest api machine learning"
    score = compute_tfidf_similarity(text, text)
    assert score == pytest.approx(1.0, abs=0.01)


def test_tfidf_similarity_unrelated():
    jd = "python developer machine learning scikit-learn"
    resume = "chef cooking baking restaurant kitchen"
    score = compute_tfidf_similarity(jd, resume)
    assert score < 0.2


def test_rank_candidates_order():
    candidates = [
        {'filename': 'a.pdf', 'final_score': 55.0},
        {'filename': 'b.pdf', 'final_score': 80.0},
        {'filename': 'c.pdf', 'final_score': 70.0},
    ]
    ranked = rank_candidates(candidates)
    assert ranked[0]['filename'] == 'b.pdf'
    assert ranked[0]['rank'] == 1
    assert ranked[1]['filename'] == 'c.pdf'
    assert ranked[2]['filename'] == 'a.pdf'


def test_rank_candidates_assigns_rank():
    candidates = [{'filename': 'x.pdf', 'final_score': 90.0}]
    ranked = rank_candidates(candidates)
    assert ranked[0]['rank'] == 1
