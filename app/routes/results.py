from flask import Blueprint, render_template, session, redirect, url_for

results_bp = Blueprint('results', __name__)

@results_bp.route('/results')
def show_results():
    results = session.get('results', None)
    if results is None:
        return redirect(url_for('upload.index'))
    return render_template('results.html', results=results)
