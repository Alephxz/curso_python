# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request
from PdfDocument import pdf_document, get_pdfs
from pdf_functions import create_pdf_dictionary, search_pdfs

app = Flask(__name__)

# Cargar PDFs y crear diccionarios
print("Cargando PDFs...")
pdf_dictionary_raw = get_pdfs()
pdfs_list = list(pdf_dictionary_raw.values())
pdf_dict = create_pdf_dictionary(pdfs_list)
print("¡Carga completa!")

@app.route('/')
def index():
    return render_template('new_index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Buscador unificado para oraciones o palabras
    if request.method == 'POST':
        query = request.form['query']
        results = search_pdfs(pdfs_list, query)
        return render_template('search.html', pdfs_list=results, query_text=query)
    else:
        # Formatear el estado por defecto para que coincida con [{'pdf': pdf, 'snippet': ''}]
        default_results = [{'pdf': p, 'snippet': ''} for p in pdfs_list[:10]]
        return render_template('search.html', pdfs_list=default_results)

@app.route('/pdf/<pdf_id>')
def pdf_detail(pdf_id):
    # Route for viewing PDF details
    pdf = pdf_dict.get(pdf_id)
    return render_template('cards.html', book=pdf)

if __name__ == '__main__':
    # Usamos el puerto 5001 para que no haya conflicto si corres app.py de books
    app.run(debug=True, port=5001)
