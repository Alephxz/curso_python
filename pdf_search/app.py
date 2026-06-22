# pyrefly: ignore [missing-import]
import os
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, flash
from PdfDocument import pdf_document, get_pdfs
from pdf_functions import create_pdf_dictionary, search_pdfs, get_statistics
import config_manager

app = Flask(__name__)
app.secret_key = "libra_secret_key"

pdf_dict = {}
pdfs_list = []

def load_pdfs_from_config():
    global pdf_dict, pdfs_list
    pdf_dict.clear()
    pdfs_list.clear()
    config_urls = config_manager.get_urls()
    for item in config_urls:
        if item.get("scraped"):
            for filename in item.get("files", []):
                downloaded_file = os.path.join("downloaded_pdfs", filename)
                markdown_file = os.path.join("markdown_files", f"{os.path.splitext(filename)[0]}.md")
                if os.path.exists(downloaded_file):
                    pdf_doc = pdf_document(item["url"], downloaded_file, markdown_file)
                    pdf_dict[filename] = pdf_doc
                    pdfs_list.append(pdf_doc)

print("Cargando PDFs desde configuración local...")
load_pdfs_from_config()
print("¡Carga completa!")

@app.route('/')
def index():
    stats = get_statistics(pdfs_list)
    return render_template('new_index.html', stats=stats)

@app.route('/scrapper')
def scrapper():
    urls = config_manager.get_urls()
    return render_template('scrapper.html', urls=urls)

@app.route('/scrapper/scrape', methods=['POST'])
def scrapper_scrape():
    url_to_scrape = request.form['url']
    print(f"Scraping URL: {url_to_scrape}")
    new_pdfs = get_pdfs(url_to_scrape)
    if new_pdfs:
        filenames = list(new_pdfs.keys())
        config_manager.update_url_scraped(url_to_scrape, filenames)
        load_pdfs_from_config()
        flash(f"Scrapeo exitoso. Se encontraron {len(filenames)} documentos.", "success")
    else:
        flash("No se encontraron PDFs o hubo un error al escrapear.", "danger")
    return redirect(url_for('scrapper'))

@app.route('/config')
def configuration():
    urls = config_manager.get_urls()
    return render_template('configuration.html', urls=urls)

@app.route('/config/add', methods=['POST'])
def config_add():
    new_url = request.form['url']
    if new_url:
        if config_manager.add_url(new_url):
            flash("URL agregada exitosamente.", "success")
        else:
            flash("La URL ya existe en la configuración.", "warning")
    return redirect(url_for('configuration'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        method = request.form.get('method', 'exact')
        results = search_pdfs(pdfs_list, query, method=method)
        return render_template('search.html', pdfs_list=results, query_text=query, method=method)
    else:
        default_results = [{'pdf': p, 'snippet': '', 'similarity': 0} for p in pdfs_list[:10]]
        return render_template('search.html', pdfs_list=default_results)

@app.route('/pdf/<pdf_id>')
def pdf_detail(pdf_id):
    pdf = pdf_dict.get(pdf_id)
    return render_template('cards.html', book=pdf)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
