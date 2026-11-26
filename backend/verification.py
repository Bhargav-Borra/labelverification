import cv2
import pytesseract

from image_processor import preprocess_image
from field_extractor import extract_fields
from validator import validate_label


# Step 1: Connect Python with Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Step 2: Create the main verification function
def verify_label_image(image_path):

    # Read the uploaded image
    image = cv2.imread(image_path)

    if image is None:
        return {"error": "Unable to read image"}

    # Step 3: Preprocess the image
    processed_images = preprocess_image(image)

    # Step 4: Perform OCR on three image versions
    ocr_results = {
        "Original Image": pytesseract.image_to_string(image),
        "Normal Threshold": pytesseract.image_to_string(
            processed_images["threshold"]
        ),
        "Adaptive Threshold": pytesseract.image_to_string(
            processed_images["adaptive"]
        )
    }

    # Step 5: Calculate how many fields each OCR result detects
    scores = {}
    extracted_results = {}

    for method, text in ocr_results.items():

        fields = extract_fields(text)

        detected_count = sum(
            value is not None and value.strip() != ""
            for value in fields.values()
        )

        scores[method] = detected_count
        extracted_results[method] = fields

    # Step 6: Select the OCR result with the most detected fields
    best_method = max(scores, key=scores.get)

    best_text = ocr_results[best_method]
    extracted_fields = extracted_results[best_method]

    # Step 7: Validate the extracted fields
    validation_results = validate_label(extracted_fields)

    # Step 8: Return the complete result
    return {
        "selected_method": best_method,
        "detected_field_count": scores[best_method],
        "ocr_text": best_text,
        "extracted_fields": extracted_fields,
        "validation": validation_results
    }


# Step 9: Test this module independently
if __name__ == "__main__":

    result = verify_label_image(
        "backend/uploads/test_label.bmp"
    )

    print("\n========== VERIFICATION RESULT ==========")

    for key, value in result.items():
        print(key, ":", value)