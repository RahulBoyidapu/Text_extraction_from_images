import cv2
import numpy as np
import pytesseract
from flask import Flask, render_template, request

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

# Function to extract text from an image
def extract_text_from_image(image, lang='eng'):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply image preprocessing techniques (adjust according to your needs)
    gray = cv2.medianBlur(gray, 3)  # Apply median blur to reduce noise
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Use Pytesseract to extract text from the image
    text = pytesseract.image_to_string(gray, lang=lang)
    return text

# Function to process an uploaded image
def process_uploaded_image(file):
    # Read the uploaded image file
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is not None:
        # Extract text from the image
        text = extract_text_from_image(image, lang='eng')
        return text
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            # Process the uploaded image file
            text = process_uploaded_image(file)
            if text is not None:
                return render_template('index.html', text=text)
            else:
                return render_template('index.html', error='Failed to process the image.')
        else:
            return render_template('index.html', error='No file uploaded.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
