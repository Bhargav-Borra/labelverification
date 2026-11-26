
import pytesseract
import cv2

# Step 1: Connect Python with Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Step 2: Read the image
image = cv2.imread("dataset/raw_images/test_label.bmp")

# Step 3: Check whether image is loaded
if image is None:
    print("Error: Image not found!")
else:
    # Step 4: Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)

    # Step 5: Display extracted text
    print("Extracted Text:")
    print(extracted_text)
