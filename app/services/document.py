import requests
from PyPDF2 import PdfReader
from docx import Document
import os
import google.generativeai as genai

class DocumentService:
    def __init__(self, genai_module):
        self.genai = genai_module

    async def summarize_file(self, file_path: str, filename: str):
        try:
            # Extract text based on file type
            text = self._extract_text_from_file(file_path, filename)
            
            # Summarize using Gemini
            model = self.genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"Please provide a comprehensive summary of the following document:\n\n{text[:8000]}"
            )
            
            return {
                "summary": response.text
            }
            
        except Exception as e:
            return {
                "summary": f"Error summarizing document: {str(e)}"
            }

    async def summarize_url(self, url: str):
        try:
            # Fetch content from URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Simple text extraction
            text = response.text[:8000]
            
            # Summarize using Gemini
            model = self.genai.GenerativeModel('gemini-1.5-flash')
            gemini_response = model.generate_content(
                f"Please provide a comprehensive summary of the content from this webpage:\n\n{text}"
            )
            
            return {
                "summary": gemini_response.text
            }
            
        except Exception as e:
            return {
                "summary": f"Error summarizing URL: {str(e)}"
            }

    def _extract_text_from_file(self, file_path: str, filename: str):
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_ext in ['.doc', '.docx']:
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def _extract_from_pdf(self, file_path: str):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")

    def _extract_from_docx(self, file_path: str):
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")
