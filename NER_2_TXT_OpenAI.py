import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from openai import AzureOpenAI

# Load API key from file
with open(r"C:\Users\MarkPoe_qkj3juw\GPT_API.txt") as file:
    api_key = file.read().strip()

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,  
    azure_endpoint="https://gpt4ce.openai.azure.com",  
    api_version="2024-02-01"
)

# Set the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract\tesseract.exe'

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

# Function to perform OCR on image-based PDFs
def ocr_image_based_pdf(pdf_path):
    # Convert PDF pages to images, specify the path to Poppler's bin folder
    poppler_path = r"C:\Poppler\poppler-24.08.0\Library\bin"
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    ocr_text = ""
    for image in images:
        # Perform OCR on each image
        ocr_text += pytesseract.image_to_string(image)
    return ocr_text

# Function to detect if a PDF is image-based or text-based
def is_pdf_image_based(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return len(text.strip()) == 0  # If no text, assume image-based

# Function to perform NER and structured graph interpretation using Azure OpenAI
def perform_ner_with_azure_openai(text_chunk):
    completion = client.chat.completions.create(
        model="gpt4ce",  
        messages=[
            {
                "role": "user",
                "content": f"""
                You are an expert in cybersecurity data. Generate a STIX compliant structured graph interpretation and extract entities for the following text:
                {text_chunk}
                """
            },
        ],
        max_tokens=2000  
    )
    return completion.choices[0].message.content

# Main logic
def main():
    pdf_path = r"C:\Users\MarkPoe_qkj3juw\Downloads\aa23-250a-apt-actors-exploit-cve-2022-47966-and-cve-2022-42475_1.pdf"
    output_path = r"C:\Users\MarkPoe_qkj3juw\Downloads\NER_STIX_Output.txt"  

    # Detect if the PDF is image-based or text-based
    if is_pdf_image_based(pdf_path):
        print("PDF is image-based. Performing OCR...")
        pdf_text = ocr_image_based_pdf(pdf_path)
    else:
        print("PDF is text-based. Extracting text...")
        pdf_text = extract_text_from_pdf(pdf_path)

    # Split text into manageable chunks for the API (if needed)
    chunk_size = 2000  
    chunks = [pdf_text[i:i + chunk_size] for i in range(0, len(pdf_text), chunk_size)]

    # Write the results to a text file with UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for chunk in chunks:
            entities = perform_ner_with_azure_openai(chunk)
            output_file.write(f"Entities and structured graph interpretation:\n{entities}\n\n")

    print(f"NER and entity linking results have been written to {output_path}")

if __name__ == "__main__":
    main()
