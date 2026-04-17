from flask import Blueprint, request, redirect, url_for, render_template, session, current_app
import os
from app.services.parser import extract_text_from_pdf
from app.services.preprocessor import preprocess_text
from app.services.tfidf_model import compute_tfidf_similarity
from app.services.bert_model import compute_bert_similarity
from app.services.ranker import rank_candidates

match_bp = Blueprint('match', __name__)

@match_bp.route('/match', methods=['GET'])
def jd_input():
    return render_template('jd_input.html')

@match_bp.route('/match', methods=['POST'])
def run_matching():
    job_description = request.form.get('job_description', '').strip()
    use_bert = False
    if not job_description:
        return render_template('jd_input.html', error='Please enter a job description.')

    upload_folder = current_app.config['UPLOAD_FOLDER']
    pdf_files = [f for f in os.listdir(upload_folder) if f.endswith('.pdf')]

    if not pdf_files:
        return render_template('jd_input.html', error='No resumes found. Please upload resumes first.')

    results = []
    jd_clean = preprocess_text(job_description)

    for pdf_file in pdf_files:
        filepath = os.path.join(upload_folder, pdf_file)
        try:
            raw_text = extract_text_from_pdf(filepath)
            clean_text = preprocess_text(raw_text)

            tfidf_score = compute_tfidf_similarity(jd_clean, clean_text)
            bert_score = compute_bert_similarity(job_description, raw_text) if use_bert else None

            final_score = bert_score if use_bert else tfidf_score

            results.append({
                'filename': pdf_file,
                'tfidf_score': round(tfidf_score * 100, 2),
                'bert_score': round(bert_score * 100, 2) if bert_score else None,
                'final_score': round(final_score * 100, 2),
                'raw_text_preview': raw_text[:300] + '...' if len(raw_text) > 300 else raw_text
            })
        except Exception as e:
            results.append({
                'filename': pdf_file,
                'error': str(e),
                'final_score': 0
            })

    ranked = rank_candidates(results)
    session['results'] = ranked

    return redirect(url_for('results.show_results'))
