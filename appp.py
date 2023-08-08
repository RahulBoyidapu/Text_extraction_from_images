import cv2
import numpy as np
import pytesseract
import spacy
import streamlit as st

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

# Load the spaCy English model for NER
nlp = spacy.load("en_core_web_sm")

# Function to extract text from an image
def extract_text_from_image(image, lang='eng'):
    # ... (your existing image processing code)

# Function to perform NER on the extracted text
 def perform_ner(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# Function to preprocess the uploaded image
def preprocess_uploaded_image(file):
    # ... (your existing image preprocessing code)

# Streamlit app
 def main():
    st.title("Image Text Extraction")
    st.write("Upload an image to extract text.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Preprocess the uploaded image file
        processed_image = preprocess_uploaded_image(uploaded_file)
        if processed_image is not None:
            # Extract text from the processed image
            text = extract_text_from_image(processed_image, lang='eng')
            # Perform NER on the extracted text
            entities = perform_ner(text)

            st.header("Extracted Text:")
            st.text(text)

            st.header("Named Entities:")
            for entity, label in entities:
                st.text(f"{entity} ({label})")
        else:
            st.error("Failed to process the image.")

if __name__ == '__main__': 
    main()