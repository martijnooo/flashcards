import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document

def read_word(document):
    # Read the .docx file
    doc = Document(document)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def split_text(sample_text: str, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(sample_text)

def safe_parse_json(text: str):
    """Parse JSON safely and extract the valid part if mixed with extra text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        print("⚠️ Could not parse JSON. Raw output below:\n", text)
        return []
