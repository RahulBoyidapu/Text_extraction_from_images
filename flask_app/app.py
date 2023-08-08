import cv2
import numpy as np
import pytesseract
import spacy
from flask import Flask, render_template, request

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

# Load the spaCy English model for NER
nlp = spacy.load("en_core_web_sm")

# Function to extract text from an image
def extract_text_from_image(image, lang='eng'):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Additional preprocessing techniques
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)  # Denoising
    gray = cv2.equalizeHist(gray)  # Histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)  # Adaptive histogram equalization
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Gaussian smoothing

    # Apply binary thresholding using Otsu's method
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Use Pytesseract to extract text from the binary image
    text = pytesseract.image_to_string(binary, lang=lang)
    return text

# Function to perform NER on the extracted text
def perform_ner(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# Function to preprocess the uploaded image
def preprocess_uploaded_image(file):
    # Read the uploaded image file
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is not None:
        # Apply preprocessing techniques to the image
        # Add your preprocessing steps here
        processed_image = image
        
        return processed_image
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            # Check if the file name has an extension
            file_extension = file.filename.rsplit('.', 1)
            if len(file_extension) > 1:
                file_extension = file_extension[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png']:
                    # Preprocess the uploaded image file
                    processed_image = preprocess_uploaded_image(file)
                    if processed_image is not None:
                        # Extract text from the processed image
                        text = extract_text_from_image(processed_image, lang='eng')
                        # Perform NER on the extracted text
                        entities = perform_ner(text)
                        return render_template('index.html', text=text, entities=entities)
                    else:
                        return render_template('index.html', error='Failed to process the image.')
                else:
                    return render_template('index.html', error='Invalid file format. Only image (jpg, jpeg, png) files are accepted.')
            else:
                return render_template('index.html', error='Invalid file name. Please make sure the file has an extension.')
        else:
            return render_template('index.html', error='No file uploaded.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
# Function to process an image
def process_image(file_path):
    # Load the image from file path
    image = cv2.imread(file_path)

    if image is not None:
        # Extract text from the image
        text = extract_text_from_image(image, lang='eng')
        # Print the extracted text
        if text.strip():
            print("Image Text:")
            print(text)
        else:
            print("No text found in the image.")
    else:
        print("Failed to load the image.")

# Prompt the user for the image file path
file_path = input("Enter the path of the image file: ")

# Process the image file
process_image(file_path)
