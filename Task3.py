import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\Tesseract\tesseract.exe"

def extract_text_from_image(image, lang='eng'):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction and text enhancement techniques
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)  # Denoising
    gray = cv2.equalizeHist(gray)  # Histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)  # Adaptive histogram equalization
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Gaussian smoothing

    # Additional noise reduction using bilateral filtering
    bilateral_filtered = cv2.bilateralFilter(blurred, 9, 75, 75)

    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(bilateral_filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Use Pytesseract to extract text from the binary image
    text = pytesseract.image_to_string(binary, lang=lang)
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