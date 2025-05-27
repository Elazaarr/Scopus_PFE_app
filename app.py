from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from main import run_search
import os

app = Flask(__name__)
app.secret_key = 'secret-key'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        method = request.form.get('method')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        scopus_id = request.form.get('scopus_id')
        year = request.form.get('year')
        export_type = request.form.get('export_type')

        try:
            result = run_search(
                method=method,
                first_name=first_name,
                last_name=last_name,
                scopus_id=scopus_id,
                year=year,
                export_type=export_type
            )

            pdf_file = result['pdf_file']
            excel_file = result['excel_file']

            return render_template('result.html',
                                   name=result['name'],
                                   total=result['total'],
                                   pdf_file=pdf_file,
                                   excel_file=excel_file)

        except Exception as e:
            flash(f"Erreur : {str(e)}", 'danger')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
