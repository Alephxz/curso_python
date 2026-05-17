""" PdfDocument.py
    Contains the pdf_document class and loader function
    adapted from Book.py
"""
import os
import requests
from bs4 import BeautifulSoup
from markitdown import MarkItDown

class pdf_document:
    def __init__(self, url, download_path, markdown_path):
        self.url = url
        self.download_path = download_path
        self.markdown_path = markdown_path
        self.content = None
        self.convert_pdf_to_markdown()

    def convert_pdf_to_markdown(self):
        try:
            converter = MarkItDown()
            result = converter.convert(self.download_path)
            markdown_content = result.markdown or result.text_content
            with open(self.markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            self.content = markdown_content    
        except Exception as e:
            print(f"Error converting PDF to Markdown: {e}")

    @property
    def title(self):
        return self.download_path.split('/')[-1].split('\\')[-1]

    @property
    def author(self):
        return "PDF"

    @property
    def genre(self):
        return "Document"

    @property
    def image_url(self):
        return "https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg"
        
    @property
    def id(self):
        return self.title

    def __str__(self):
        filename = self.download_path.split('/')[-1].split('\\')[-1]
        return f"PDF: {filename} - {self.url}"

def get_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None 
    
def extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links

def download_pdf(url, filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")

def get_pdfs(url="https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"):
    download_path = "downloaded_pdfs"
    markdown_path = "markdown_files"
    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)
    if not os.path.exists(markdown_path):
        os.makedirs(markdown_path, exist_ok=True)
        
    html = get_webpage(url)
    if not html:
        print(f"Failed to fetch the webpage: {url}")
        return {}
        
    pdf_links = extract_pdf_links(html)
    pdf_dict = {}
    for link in pdf_links:
        filename = link.split('/')[-1]
        downloaded_file = os.path.join(download_path, filename) 
        download_pdf(link, f"{downloaded_file}")
        markdown_file = os.path.join(markdown_path, f"{os.path.splitext(filename)[0]}.md")
        pdf_doc = pdf_document(link, downloaded_file, markdown_file)
        pdf_dict[filename] = pdf_doc
        print(f"Downloaded: {downloaded_file}")
    return pdf_dict
