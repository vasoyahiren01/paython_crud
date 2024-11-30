import base64
import re
import io
from PIL import Image
from pdf2image import convert_from_bytes
import easyocr
import requests

# Your Lambda function code

def extract_aadhar_details(text):
    aadhar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"
    matches = re.findall(aadhar_pattern, text)
    return matches[0] if matches else None

def extract_pan_details(text):
    pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
    matches = re.findall(pan_pattern, text)
    return matches[0] if matches else None

def process_image(image_data):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_data, detail=0)
    return " ".join(result)

def process_pdf(pdf_data):
    images = convert_from_bytes(pdf_data)
    reader = easyocr.Reader(['en'])
    text = ""
    for image in images:
        text += " ".join(reader.readtext(image, detail=0)) + " "
    return text

def lambda_handler(event, context):

    url = "https://files.superworks.com/files/6026168299d95542461309b6/hrms/60c6d650701f070cb64e3594/proof/qDkHnzVYrHBQ6WCY.jpeg"
    base64_data = encode_file_from_url_to_base64(url)

    # Test event data
    event = {
        "document_type": "pancard",  # or "pancard" for PAN card
        "base64_data": base64_data  # Pass the base64-encoded data here
    }
    
    document_type = event.get('document_type')
    if not document_type:
        return {"error": "document_type is required. Please specify either 'aadhar' or 'pancard'."}

    base64_data = event.get('base64_data')
    if not base64_data:
        return {"error": "Base64 data is required for the document."}

    file_data = base64.b64decode(base64_data)
    
    if file_data[:4] == b'%PDF':
        text = process_pdf(file_data)
    else:
        image = Image.open(io.BytesIO(file_data))
        text = process_image(image)
    
    if document_type.lower() == 'aadhar':
        aadhar_number = extract_aadhar_details(text)
        return {"aadhar_number": aadhar_number} if aadhar_number else {"error": "Aadhar number not found."}
    elif document_type.lower() == 'pancard':
        pan_number = extract_pan_details(text)
        print(pan_number)
        return {"pan_number": pan_number} if pan_number else {"error": "PAN number not found."}
    else:
        return {"error": "Invalid document_type. Use 'aadhar' or 'pancard'."}

# Encoding a local file to base64
def encode_file_to_base64(filepath):
    with open(filepath, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def encode_file_from_url_to_base64(url):
    # Download the file from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the download was successful
    
    # Encode the content of the file in base64
    encoded_string = base64.b64encode(response.content).decode('utf-8')
    return encoded_string


# Call lambda_handler
response = lambda_handler({}, None)
print(response)
