""" pdf_functions.py
    Contains functions to work with pdf_document objects
    adapted from book_functions.py
"""

from PdfDocument import pdf_document, get_pdfs
import re

def get_urls(pdfs: list[pdf_document]) -> list[str]:
    """Get all unique URLs from a list of pdf_document objects"""
    urls = set()
    for pdf in pdfs:
        urls.add(pdf.url)
    return sorted(list(urls))

def create_chunk_dictionary(pdfs: list[pdf_document]) -> dict[str, list[pdf_document]]:
    """Create a dictionary of text chunks and their corresponding pdfs"""
    chunk_dict = {}
    for pdf_doc in pdfs:
        content = pdf_doc.content
        if not content:
            continue
        chunks_length = 20
        chunks = [content[i:i+chunks_length] for i in range(0, len(content), chunks_length)]
        for chunk in chunks:
            if chunk not in chunk_dict:
                chunk_dict[chunk] = []
            if pdf_doc not in chunk_dict[chunk]:
                chunk_dict[chunk].append(pdf_doc)
    return chunk_dict

def create_word_dictionary(pdfs: list[pdf_document]) -> dict[str, list[pdf_document]]:
    """Create a dictionary of words and their corresponding pdfs"""
    word_dict = {}
    for pdf_doc in pdfs:
        content = pdf_doc.content
        if not content:
            continue
        words = content.split()
        for word in words:
            word = word.lower().strip('.,()[]"\'')
            if not word:
                continue
            if word not in word_dict:
                word_dict[word] = []
            if pdf_doc not in word_dict[word]:
                word_dict[word].append(pdf_doc)
    return word_dict

def create_pdf_dictionary(pdf_list: list[pdf_document]) -> dict[str, pdf_document]:
    """Create a dictionary of pdfs using their filename as key"""
    pdf_dict = {}
    for pdf in pdf_list:
        # Extraemos el nombre del archivo de la ruta
        filename = pdf.download_path.split('/')[-1].split('\\')[-1]
        pdf_dict[filename] = pdf
    return pdf_dict

def search_pdfs(pdfs: list[pdf_document], query: str) -> list[dict]:
    """Search for a phrase or words in the PDFs and return the pdf and a snippet"""
    results = []
    query_lower = query.lower().strip()
    if not query_lower:
        return results
        
    for pdf in pdfs:
        if not pdf.content:
            continue
        content_lower = pdf.content.lower()
        idx = content_lower.find(query_lower)
        if idx != -1:
            # Extraer un fragmento alrededor de la coincidencia
            start = max(0, idx - 40)
            end = min(len(pdf.content), idx + len(query_lower) + 40)
            snippet = pdf.content[start:end]
            
            # Poner puntos suspensivos si cortamos el texto
            if start > 0:
                snippet = "..." + snippet
            if end < len(pdf.content):
                snippet = snippet + "..."
                
            # Subrayar (resaltar) la palabra buscada manteniendo sus mayúsculas/minúsculas originales
            escaped_query = re.escape(query.strip())
            highlighted_snippet = re.sub(f"({escaped_query})", r"<mark>\1</mark>", snippet, flags=re.IGNORECASE)
            
            results.append({
                'pdf': pdf,
                'snippet': highlighted_snippet
            })
    return results

if __name__ == "__main__":
    # get_pdfs() returns a dictionary, so we convert it to a list of values
    pdf_dictionary = get_pdfs()
    pdfs_list = list(pdf_dictionary.values())
    
    print("URLs encontradas:")
    print(get_urls(pdfs_list))
    
    chunk_dict = create_chunk_dictionary(pdfs_list)
    print(f"\nTotal de fragmentos (chunks) creados: {len(chunk_dict)}")
    
    word_dict = create_word_dictionary(pdfs_list)
    print(f"Total de palabras únicas indexadas: {len(word_dict)}")
