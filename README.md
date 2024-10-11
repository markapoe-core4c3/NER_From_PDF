# README for PDF NER and STIX Structured Graph Interpretation Script

## Overview

This script processes PDF files, performs Optical Character Recognition (OCR) if needed, and uses Azure OpenAI to perform Named Entity Recognition (NER) and generate a structured graph interpretation of the content. It supports both text-based and image-based PDFs and outputs the extracted entities and STIX-compliant structured graph interpretation in a text file.

## Dependencies

The script requires several Python libraries and system tools to work properly:

- **Python Libraries:**
  - `PyPDF2`: For extracting text from text-based PDFs.
  - `pytesseract`: For performing OCR on image-based PDFs.
  - `pdf2image`: To convert PDF pages into images for OCR.
  - `openai`: To interact with Azure OpenAI for performing NER and generating structured graphs.
  - `boto3`: (If using S3 for file storage, optional)

- **System Tools:**
  - **Tesseract**: Required for OCR. You can download it from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
  - **Poppler**: Required by `pdf2image` for converting PDFs to images. You can download it from [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/).

## Setup Instructions

### 1. Install Python Dependencies

You can install the required Python libraries by running the following command:

```bash
pip install PyPDF2 pytesseract pdf2image openai
```

### 2. Install Tesseract

1. Download and install Tesseract from [this link](https://github.com/tesseract-ocr/tesseract).
2. After installation, note the installation path (e.g., `C:\Tesseract`).

### 3. Install Poppler

1. Download Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/).
2. Extract it to a location, for example, `C:\Poppler`.
3. Update the script to use the `bin` folder path from Poppler for OCR processing.

### 4. Configure OpenAI API

1. Note that this script stores the API key in a file (e.g., `GPT_API.txt`) - this should be an environment variable.

### 5. Optional: S3 Integration

If your PDF files are stored in an S3 bucket, install `boto3` to interact with S3, and adjust the script accordingly.

```bash
pip install boto3
```

## Running the Script

To run the script, make sure to specify the correct path to the PDF file and the output file. The script automatically detects whether the PDF is image-based or text-based and performs the appropriate extraction process.

1. Ensure the PDF file path (`pdf_path`) is set correctly in the script.
2. The output (NER and STIX structured graph) will be written to a text file specified by `output_path`.

### Example Command:

```bash
python your_script.py
```

### Functions

- **`extract_text_from_pdf(pdf_path)`**: Extracts text from a PDF if it's a text-based PDF.
- **`ocr_image_based_pdf(pdf_path)`**: Converts a PDF into images and performs OCR to extract text from image-based PDFs.
- **`is_pdf_image_based(pdf_path)`**: Determines whether the PDF is image-based or text-based by checking if any text can be extracted.
- **`perform_ner_with_azure_openai(text_chunk)`**: Sends chunks of extracted text to Azure OpenAI for NER and structured graph generation. It returns STIX-compliant structured graph interpretations and entities.
- **`main()`**: The main logic that coordinates PDF extraction, NER processing, and outputs the results to a file.

## Customization

- You can adjust the OpenAI prompt to include specific entity types or to refine the generated structured graphs.
- Modify paths to match your environment (e.g., Tesseract, Poppler, and output paths).
  
## Troubleshooting

- **Tesseract or Poppler not found**: Ensure the correct paths to Tesseract and Poppler are provided in the script.
- **OCR not working**: Ensure that Tesseract is installed and properly referenced in the script.
- **API errors**: Make sure the Azure OpenAI API key is valid and stored in the correct location.

## Output

The script generates two main types of outputs:

1. **NER and Structured Graph Interpretation**: Written to a `.txt` file (e.g., `NER_STIX_Output.txt`).
2. **STIX-compliant JSON output** (if required, this part can be extended for generating structured JSON).

---
### Customizing the OpenAI Prompt

The core of the script relies on interacting with Azure OpenAI to perform Named Entity Recognition (NER) and generate a structured graph interpretation of the PDF content. The request sent to OpenAI, called the **prompt**, is crucial in determining the quality and specificity of the output. Here's an explanation of the prompt used in this script and how you can modify it to fit your specific needs.

#### Current Prompt:
In the script, the prompt is structured as follows:

```python
{
    "role": "user",
    "content": f"""
    You are an expert in cybersecurity data. Generate a STIX-compliant structured graph interpretation and extract entities for the following text:
    {text_chunk}
    """
}
```

This prompt asks the model to:
1. Act as an expert in **cybersecurity data**.
2. Generate a **STIX-compliant structured graph interpretation**, which is relevant for creating graph databases that comply with the STIX (Structured Threat Information eXpression) standard used in cybersecurity.
3. **Extract entities** from the provided `text_chunk`, such as organizations, attack vectors, vulnerabilities, and other relevant details.

#### Customizing the Prompt:
You can modify this prompt to tailor it to your specific use case, depending on the kind of data you're working with and the structure you want to extract. Below are some possible modifications:

1. **Change the Domain**: If you are working in a different domain (e.g., healthcare, finance), you can change the prompt to ask for expertise in that specific domain:
   ```python
   "You are an expert in healthcare data. Generate a structured graph interpretation and extract medical entities for the following text:"
   ```

2. **Modify the Output Format**: You may want a different type of structured graph output or specific formats. For example:
   ```python
   "Generate a graph interpretation using a hierarchical format that highlights key relationships between entities in the following text:"
   ```

3. **Focus on Specific Entities**: You can ask the model to extract particular types of entities, such as malware names, CVEs, or legal terms:
   ```python
   "Extract the names of malware, CVE numbers, and organizations involved from the following text:"
   ```

4. **Change Graph Structure**: If STIX is not required, you can ask for a different graph format or relationship structure:
   ```python
   "Generate a relationship graph with nodes representing people, organizations, and events, and edges representing interactions between them."
   ```

5. **Enhance Contextual Awareness**: You can provide more background in the prompt to guide the model to focus on particular nuances or relationships:
   ```python
   "Given the context of a cybersecurity incident, extract entities and generate a structured graph highlighting the attack vector, the impacted systems, and mitigation strategies."
   ```

#### Example of an Extended Custom Prompt:

Here’s an example of how you might expand the current prompt for deeper analysis:

```python
{
    "role": "user",
    "content": f"""
    You are an expert in cybersecurity data. Please extract the following from the text:
    1. Names of known malware, threat actors, or attack vectors.
    2. CVE numbers associated with any vulnerabilities mentioned.
    3. Dates of incidents or investigations.
    
    Also, generate a STIX-compliant structured graph showing the relationships between the identified entities. The nodes should represent the entities, and the edges should describe their interactions (e.g., 'exploits', 'targets', 'investigates'). Ensure that the graph is structured to highlight the flow of an attack from identification to mitigation.
    """
}
```

### Why Customizing the Prompt Matters:
- **Accuracy**: A well-crafted prompt improves the accuracy of entity extraction by giving the model clearer instructions about the domain and expected output.
- **Relevance**: Customizing the prompt ensures that the output is aligned with your specific needs, whether it's extracting malware names, financial terms, or legal documents.
- **Flexibility**: You can change the structure of the prompt to generate different kinds of outputs, from detailed reports to structured graphs and relationship mappings.

By tailoring the prompt to your domain and output requirements, you can get more meaningful and precise results from the Azure OpenAI model.
With the above setup, you can easily extract structured data from text-based and image-based PDFs and output structured graph interpretations for further analysis or import into graph databases.
