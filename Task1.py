import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

# Function to extract text from an image
def extract_text_from_image(image, lang='eng'):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply image preprocessing techniques
    gray = cv2.medianBlur(gray, 3)  # Apply median blur to reduce noise
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Use Pytesseract to extract text from the image
    text = pytesseract.image_to_string(gray, lang=lang)
    return text

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
