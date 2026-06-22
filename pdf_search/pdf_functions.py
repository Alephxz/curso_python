""" pdf_functions.py
    Contains functions to work with pdf_document objects
    adapted from book_functions.py
"""

from PdfDocument import pdf_document, get_pdfs
import re

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

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

def get_statistics(pdfs: list[pdf_document]) -> dict:
    total_docs = len(pdfs)
    total_words = 0
    docs_per_year = {}
    
    for pdf in pdfs:
        # Contar palabras
        if pdf.content:
            total_words += len(pdf.content.split())
        
        # Extraer año de la URL
        match = re.search(r'\b(19|20)\d{2}\b', pdf.url)
        if match:
            year = match.group(0)
        else:
            year = "Unknown"
            
        docs_per_year[year] = docs_per_year.get(year, 0) + 1
        
    return {
        "total_docs": total_docs,
        "total_words": total_words,
        "docs_per_year": docs_per_year
    }

def search_pdfs(pdfs: list[pdf_document], query: str, method: str = "exact") -> list[dict]:
    """Search for a phrase or words in the PDFs and return the pdf, a snippet, and similarity %"""
    results = []
    query_lower = query.lower().strip()
    if not query_lower:
        return results
        
    for pdf in pdfs:
        if not pdf.content:
            continue
            
        if method == "exact":
            content_lower = pdf.content.lower()
            idx = content_lower.find(query_lower)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(pdf.content), idx + len(query_lower) + 40)
                snippet = pdf.content[start:end]
                
                if start > 0: snippet = "..." + snippet
                if end < len(pdf.content): snippet = snippet + "..."
                    
                escaped_query = re.escape(query.strip())
                highlighted_snippet = re.sub(f"({escaped_query})", r"<mark>\1</mark>", snippet, flags=re.IGNORECASE)
                
                results.append({
                    'pdf': pdf,
                    'snippet': highlighted_snippet,
                    'similarity': 100.0
                })
        elif method == "similar":
            # Dividir en oraciones rudimentariamente
            sentences = re.split(r'(?<=[.!?]) +|\n+', pdf.content)
            best_match = None
            best_sim = 0
            best_snippet = ""
            
            for sentence in sentences:
                if not sentence.strip():
                    continue
                # Levenshtein distance native
                dist = levenshtein_distance(query_lower, sentence.lower().strip())
                max_len = max(len(query_lower), len(sentence.strip()))
                if max_len == 0: continue
                
                sim_pct = (1 - dist / max_len) * 100
                if sim_pct > best_sim:
                    best_sim = sim_pct
                    best_snippet = sentence
                    
            if best_sim > 30: # Umbral de similitud
                escaped_query = re.escape(query.strip())
                # Tratar de resaltar palabras parecidas es complejo, resaltamos lo exacto si hay, 
                # o mostramos el snippet tal cual
                highlighted_snippet = best_snippet
                
                results.append({
                    'pdf': pdf,
                    'snippet': f"...{highlighted_snippet}...",
                    'similarity': round(best_sim, 3)
                })
                
    # Sort by similarity descending
    results.sort(key=lambda x: x['similarity'], reverse=True)
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
