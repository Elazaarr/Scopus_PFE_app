from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from main import run_search
import os
import re

app = Flask(__name__)
app.secret_key = 'secret-key'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search", methods=['GET','POST'])
def search():
    method = request.args.get("method")
    if request.method == "GET":
        return render_template("search.html", method=method)
    elif request.method == "POST":
        # Récupérer les données du formulaire
        if method == "name":
            name = request.form.get("name")
            # logique avec name
        elif method == "scopus":
            scopus_id = request.form.get("scopus_id")
            # logique avec scopus_id
        # retourne un résultat ou redirige
        return "traitement terminé"

@app.route('/results', methods=['POST'])
def results():
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

        # Construction du nom à afficher
        if method == 'name':
            name_display = f"{first_name} {last_name}"
        else:
            name_display = f"Scopus ID : {scopus_id}"

        # Récupération des bons fichiers
        pdf_file = result['file'].get('pdf') if 'pdf' in result['file'] else None
        excel_file = result['file'].get('excel') if 'excel' in result['file'] else None

        return render_template('results.html',
                               name=name_display,
                               publications=result['data'],
                               total=len(result['data']),
                               pdf_file=pdf_file,
                               excel_file=excel_file,
                               export_type=export_type)

    except Exception as e:
        flash(f"Erreur : {str(e)}", 'danger')
        return redirect(url_for('home'))

@app.route('/download/<path:filename>')
def download_file(filename):
    # Remove 'output/' from filename if it exists
    if filename.startswith('output/'):
        filename = filename[7:]  # Remove 'output/' prefix
    
    file_path = os.path.join(UPLOAD_FOLDER, 'output', filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        flash(f"File not found: {filename}", 'danger')
        return redirect(url_for('home'))
    
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)