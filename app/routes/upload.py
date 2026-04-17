from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
import os

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@upload_bp.route('/upload', methods=['POST'])
def upload_resumes():
    if 'resumes' not in request.files:
        flash('No files selected', 'error')
        return redirect(url_for('upload.index'))

    files = request.files.getlist('resumes')
    uploaded = []

    for file in files:
        if file and allowed_file(file.filename):
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded.append(filename)

    if not uploaded:
        flash('No valid PDF files uploaded', 'error')
        return redirect(url_for('upload.index'))

    flash(f'{len(uploaded)} resume(s) uploaded successfully!', 'success')
    return redirect(url_for('match.jd_input'))
