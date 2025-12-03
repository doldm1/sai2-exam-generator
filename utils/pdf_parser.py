"""
PDF parsing utilities using PyMuPDF (fitz).
Extracts text content page by page from PDF files.
"""

import fitz  # PyMuPDF
from typing import Dict, Tuple, List
import os
import re


def extract_text_from_pdf(pdf_path: str) -> Tuple[Dict[int, str], int]:
    """
    Extract text from a PDF file, page by page.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Tuple of (dictionary mapping page numbers to text content, total pages)
        Page numbers start at 1 (not 0) for user-friendliness
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If PDF cannot be opened or parsed
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    pages_content = {}
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Clean up the text (remove excessive whitespace)
            text = clean_text(text)
            
            # Store with 1-based page numbering
            pages_content[page_num + 1] = text
        
        total_pages = len(doc)
        doc.close()
        
        return pages_content, total_pages
    
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and normalizing.
    
    Args:
        text: Raw text extracted from PDF
    
    Returns:
        Cleaned text
    """
    # Replace multiple spaces with single space
    text = " ".join(text.split())
    
    # Remove excessive newlines (keep paragraph structure)
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    text = '\n'.join(lines)
    
    return text


def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from PDF file.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Dictionary containing PDF metadata
    """
    try:
        doc = fitz.open(pdf_path)
        metadata = {
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', ''),
            'pages': len(doc),
            'file_size': os.path.getsize(pdf_path)
        }
        doc.close()
        return metadata
    except Exception as e:
        return {'error': str(e)}


def extract_page_text(pdf_path: str, page_number: int) -> str:
    """
    Extract text from a specific page.
    
    Args:
        pdf_path: Path to the PDF file
        page_number: Page number (1-based indexing)
    
    Returns:
        Text content of the page
    """
    try:
        doc = fitz.open(pdf_path)
        
        # Convert to 0-based indexing
        page = doc[page_number - 1]
        text = page.get_text()
        text = clean_text(text)
        
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting page {page_number}: {str(e)}"


def extract_learning_objectives(pages_content: Dict[int, str]) -> List[str]:
    """
    Extract learning objectives from the first few pages of course material.
    
    Args:
        pages_content: Dictionary mapping page numbers to text content
    
    Returns:
        List of detected learning objective strings
    """
    objectives = []
    
    # Define patterns to detect learning objectives sections (German and English)
    section_patterns = [
        r'lernziele?[:.\s]',
        r'learning objectives?[:.\s]',
        r'learning outcomes?[:.\s]',
        r'nach diesem (kapitel|modul|kurs)',
        r'after this (chapter|module|course)',
        r'by the end of this',
        r'students? (will|can|should)',
        r'you (will|can|should)',
        r'sie können',
        r'main learning (outcomes?|objectives?)',
    ]
    
    # Look at first 3 pages (objectives usually at beginning)
    pages_to_check = sorted([p for p in pages_content.keys() if p <= 3])
    
    for page_num in pages_to_check:
        text = pages_content[page_num]
        text_lower = text.lower()
        
        # Check if this page contains a learning objectives section
        section_found = any(re.search(pattern, text_lower) for pattern in section_patterns)
        
        if section_found:
            # Extract bullet points or numbered items that look like learning objectives
            # Match lines that start with bullet, number, or "You can/Sie können"
            objective_patterns = [
                r'(?:^|\n)[\s]*[•\-\*●]\s*(.+?)(?:\n|$)',  # Bullet points
                r'(?:^|\n)[\s]*\d+[\.\)]\s*(.+?)(?:\n|$)',  # Numbered lists
                r'(?:^|\n)[\s]*(You (?:can|will|should) .+?)(?:\n|$)',  # "You can..."
                r'(?:^|\n)[\s]*(Sie können .+?)(?:\n|$)',  # "Sie können..."
                r'(?:^|\n)[\s]*(Students? (?:will|can|should) .+?)(?:\n|$)',  # "Students will..."
            ]
            
            for pattern in objective_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    obj = match.group(1).strip()
                    # Filter: must be substantial (10-300 chars) and not too generic
                    if 10 <= len(obj) <= 300 and obj not in objectives:
                        # Clean up: remove common prefixes
                        obj = re.sub(r'^(You can|Sie können|Students? (?:will|can|should))\s+', '', obj, flags=re.IGNORECASE)
                        objectives.append(obj)
    
    # Return up to 5 unique objectives
    return objectives[:5]