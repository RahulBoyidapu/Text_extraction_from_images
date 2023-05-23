import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

def preprocess_image(image):
    # Resize the image to a larger size
    resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Convert the resized image to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to enhance text visibility
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Apply additional preprocessing steps as needed (e.g., denoising, image enhancement)
    # ...
    return thresholded

def extract_text_from_image(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)
        # Preprocess the image
        processed_image = preprocess_image(image)
        # Use Pytesseract to extract text from the processed image
        text = pytesseract.image_to_string(processed_image, lang='eng')
        return text
    except Exception as e:
        print("Error occurred during text extraction:")
        print(e)
        return None

# Prompt the user for the image path
image_path = input("Enter the path to the image: ")
extracted_text = extract_text_from_image(image_path)

if extracted_text:
    print("Text extracted from the image:")
    print(extracted_text)
