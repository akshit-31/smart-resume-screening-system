"""
Resume Roast Blueprint
GET  /roast/<filename> → render roast page
POST /roast/<filename> → call Claude, return JSON {roast, fixed}
"""

from flask import Blueprint, render_template, request, session, current_app, jsonify
import os
from app.services.parser import extract_text_from_pdf
from app.services.roast_generator import generate_roast, format_roast_for_download

roast_bp = Blueprint('roast', __name__)


@roast_bp.route('/roast/<filename>', methods=['GET'])
def roast_page(filename):
    """Render the roast page for a given resume"""
    if '..' in filename or '/' in filename or '\\' in filename:
        return "Invalid filename", 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)

    if not os.path.exists(filepath):
        return "Resume not found", 404

    job_description = session.get('job_description', '')

    return render_template(
        'roast.html',
        filename=filename,
        job_description=job_description
    )


@roast_bp.route('/roast/<filename>', methods=['POST'])
def roast_resume(filename):
    """Generate roast + fixed version via Claude API, return JSON"""
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'success': False, 'error': 'Invalid filename'}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)

    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'Resume file not found'}), 404

    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(filepath)

        # Get JD from session
        job_description = session.get('job_description', '')
        if not job_description:
            return jsonify({
                'success': False,
                'error': 'No job description found. Please run matching first.'
            }), 400

        # Generate roast
        result = generate_roast(resume_text, job_description)

        if result['success']:
            result['download_text'] = format_roast_for_download(result['fixed'], filename)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500
