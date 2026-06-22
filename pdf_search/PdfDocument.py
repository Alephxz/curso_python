""" PdfDocument.py
    Contains the pdf_document class and loader function
    adapted from Book.py
"""
import os
import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
# pyrefly: ignore [missing-import]
from markitdown import MarkItDown
import fitz
import pytesseract
from PIL import Image
import io

class pdf_document:
    def __init__(self, url, download_path, markdown_path):
        self.url = url
        self.download_path = download_path
        self.markdown_path = markdown_path
        self.content = None
        self.convert_pdf_to_markdown()

    def convert_pdf_to_markdown(self):
        try:
            if os.path.exists(self.markdown_path):
                with open(self.markdown_path, 'r', encoding='utf-8') as f:
                    self.content = f.read()
            else:
                doc = fitz.open(self.download_path)
                full_text = ""
                
                tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                if os.path.exists(tesseract_path):
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path

                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    page_text = page.get_text()
                    
                    if len(page_text.strip()) < 50:
                        try:
                            # Resolution zoom for OCR
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                            img = Image.open(io.BytesIO(pix.tobytes("png")))
                            # Tesseract OCR extraction
                            ocr_text = pytesseract.image_to_string(img)
                            full_text += ocr_text + "\n\n"
                        except Exception as ocr_e:
                            print(f"Error OCR on page {page_num}: {ocr_e}")
                            full_text += page_text + "\n\n"
                    else:
                        full_text += page_text + "\n\n"
                
                # Fallback to markitdown if everything is empty
                if not full_text.strip():
                    converter = MarkItDown()
                    result = converter.convert(self.download_path)
                    markdown_content = result.markdown or result.text_content
                    full_text = markdown_content
                    
                with open(self.markdown_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                self.content = full_text    
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

def get_pdfs(url):
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
