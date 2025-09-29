import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file into a single string."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

def chunk_document_by_headings(document_text):
    """
    Splits a document into large chunks based on numbered headings.
    Example headings: "1 HEADING", "8.1 SUBHEADING", "11.2.1 SUB-SUBHEADING"
    """
    # This regex looks for lines starting with a number (like 1. or 8.1 or 11.)
    # followed by uppercase letters, representing the titles.
    # It handles nested numbering (e.g., 8.1, 11.2).
    pattern = r"(^\d+(\.\d+)*\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s/]+$)"
    
    # Use re.split() to break the text apart at each heading.
    # The pattern is kept as part of the resulting list.
    parts = re.split(pattern, document_text, flags=re.MULTILINE)
    
    chunks = []
    # The result of re.split with a capturing group is [text_before, separator, text_after, ...]
    # We need to reassemble the separator (the heading) with its corresponding text.
    for i in range(1, len(parts), 3):
        heading = parts[i]
        content = parts[i + 2] if (i + 2) < len(parts) else ""
        
        # We can also capture the text before the first heading, if any
        if i == 1 and parts[0].strip():
             chunks.append({"heading": "Introducción", "content": parts[0].strip()})
             
        chunks.append({"heading": heading.strip(), "content": content.strip()})
        
    return chunks

# --- Main Execution ---

# 1. Define the path to your PDF file
pdf_file_path = "embedding/company_licitations/aguas_andinas.pdf"

# 2. Extract the full text from the PDF
full_document_text = extract_text_from_pdf(pdf_file_path)

# 3. Split the text into large, structured chunks
large_chunks = chunk_document_by_headings(full_document_text)

# 4. Print the results to see the chunks
for i, chunk in enumerate(large_chunks):
    print(f"--- CHUNK {i+1}: {chunk['heading']} ---")
    # Print the first 250 characters of the content for brevity
    print(chunk['content'][:250] + "...")
    print("\n")