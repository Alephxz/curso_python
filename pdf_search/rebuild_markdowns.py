import config_manager
import os
from PdfDocument import pdf_document

pdf_dict = {}
pdfs_list = []

print("Rebuilding markdowns with OCR...")
config_urls = config_manager.get_urls()
for item in config_urls:
    if item.get("scraped"):
        for filename in item.get("files", []):
            downloaded_file = os.path.join("downloaded_pdfs", filename)
            markdown_file = os.path.join("markdown_files", f"{os.path.splitext(filename)[0]}.md")
            if os.path.exists(downloaded_file):
                print(f"Processing {filename}...")
                pdf_doc = pdf_document(item["url"], downloaded_file, markdown_file)
                pdf_dict[filename] = pdf_doc
                pdfs_list.append(pdf_doc)

print("Done rebuilding!")
