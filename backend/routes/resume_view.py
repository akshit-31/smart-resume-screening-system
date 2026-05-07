from flask import Blueprint, render_template, request, session, current_app, jsonify
import os
from backend.services.parser import extract_text_from_pdf
from backend.services.resume_analyzer import advanced_resume_analysis
from backend.services.ai_resume_generator import generate_optimized_resume, format_resume_for_download

resume_view_bp = Blueprint('resume_view', __name__)


@resume_view_bp.route('/resume/<filename>')
def view_resume(filename):
    if '..' in filename or '/' in filename or '\\' in filename:
        return "Invalid filename", 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)

    if not os.path.exists(filepath):
        return "Resume not found", 404

    try:
        raw_text       = extract_text_from_pdf(filepath)
        job_description = session.get('job_description', '')
        mode           = request.args.get('mode', 'analyze')

        # Full advanced analysis (used in analyze mode)
        analysis = advanced_resume_analysis(raw_text, job_description)

        return render_template(
            'resume_view.html',
            filename=filename,
            analysis=analysis,
            raw_text=raw_text,
            job_description=job_description,
            mode=mode
        )
    except Exception as e:
        return f"Error processing resume: {str(e)}", 500


@resume_view_bp.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        filename        = data.get('filename', '')
        original_text   = data.get('original_text', '')
        job_description = data.get('job_description') or session.get('job_description', '')

        if not original_text:
            return jsonify({'success': False, 'error': 'Original resume text is required'}), 400
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description not found. Please run matching first.'}), 400

        result = generate_optimized_resume(original_text, job_description)
        if result['success']:
            result['download_text'] = format_resume_for_download(result['optimized_resume'], filename)

        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500
