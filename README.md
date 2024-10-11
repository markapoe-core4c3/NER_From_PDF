# README for PDF NER and STIX Structured Graph Interpretation Script

## Overview
This script processes PDF files, performs Optical Character Recognition (OCR) if needed, and uses Azure OpenAI to perform Named Entity Recognition (NER) and generate a structured graph interpretation of the content. It supports both text-based and image-based PDFs and outputs the extracted entities and STIX-compliant structured graph interpretation in a text file.

## Dependencies
The script requires several Python libraries and system tools to work properly:

### Python Libraries:
- **PyPDF2**: For extracting text from text-based PDFs.
- **pytesseract**: For performing OCR on image-based PDFs.
- **pdf2image**: To convert PDF pages into images for OCR.
- **openai**: To interact with Azure OpenAI for performing NER and generating structured graphs.
- **boto3**: (Optional) If using S3 for file storage.

### System Tools:
- **Tesseract**: Required for OCR. You can download it from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
- **Poppler**: Required by `pdf2image` for converting PDFs to images. You can download it from [Poppler](http://blog.alivate.com.au/poppler-windows/).

## Setup Instructions

### 1. Install Python Dependencies
You can install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt
