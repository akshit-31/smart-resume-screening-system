import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload' in response.data


def test_jd_input_page_loads(client):
    response = client.get('/match')
    assert response.status_code == 200
    assert b'Job Description' in response.data


def test_results_redirects_without_session(client):
    response = client.get('/results')
    assert response.status_code == 302  # redirects to index


def test_upload_no_file(client):
    response = client.post('/upload', data={}, follow_redirects=True)
    assert response.status_code == 200


def test_match_empty_jd(client):
    response = client.post('/match', data={'job_description': ''})
    assert response.status_code == 200
    assert b'Please enter' in response.data
