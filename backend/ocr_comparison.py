
import cv2
import pytesseract
from image_processor import preprocess_image
from field_extractor import extract_fields
from validator import validate_label

# Step 1: Connect Python with Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Step 2: Read original image
original_image = cv2.imread(
    "dataset/raw_images/test_label.bmp"
)

# Step 3: Check original image
if original_image is None:
    print("Original image not found!")

else:

    # Step 4: Process the original image
    processed_images = preprocess_image(original_image)

    # Step 5: Get individual processed images
    threshold_image = processed_images["threshold"]
    adaptive_image = processed_images["adaptive"]

    # Step 6: Extract text from all three images
    original_text = pytesseract.image_to_string(original_image)
    threshold_text = pytesseract.image_to_string(threshold_image)
    adaptive_text = pytesseract.image_to_string(adaptive_image)

    # Step 7: Display OCR results
    print("\n========== ORIGINAL IMAGE ==========")
    print(original_text)

    print("\n========== NORMAL THRESHOLD ==========")
    print(threshold_text)

    print("\n========== ADAPTIVE THRESHOLD ==========")
    print(adaptive_text)

    # Step 8: Define expected text
    expected_fields = [
        "PRODUCT NAME: TEST WHISKY",
        "BATCH NO: B12345",
        "MFG DATE: 1-10-2026",
        "EXP DATE: 1-10-2028",
        "MRP: 750"
    ]

    # Step 9: Function to calculate accuracy
    def calculate_accuracy(actual_text, expected_fields):

        correct = 0

        for field in expected_fields:

            if field in actual_text:
                correct += 1

        total = len(expected_fields)

        accuracy = (correct / total) * 100

        print("Correct Fields:", correct, "/", total)
        print("Field Match Score:", accuracy, "%")

        return accuracy

    # Step 10: Compare all three OCR results

    print("\n========== ORIGINAL IMAGE SCORE ==========")
    original_score = calculate_accuracy(original_text, expected_fields)

    print("\n========== NORMAL THRESHOLD SCORE ==========")
    threshold_score = calculate_accuracy(threshold_text, expected_fields)

    print("\n========== ADAPTIVE THRESHOLD SCORE ==========")
    adaptive_score = calculate_accuracy(adaptive_text, expected_fields)

    # Step 11: Store scores and corresponding text
    scores = {
        "Original Image": original_score,
        "Normal Threshold": threshold_score,
        "Adaptive Threshold": adaptive_score
    }

    ocr_results = {
        "Original Image": original_text,
        "Normal Threshold": threshold_text,
        "Adaptive Threshold": adaptive_text
    }

    # Step 12: Automatically select the best OCR result
    best_method = max(scores, key=scores.get)

    best_text = ocr_results[best_method]

    print("\n========== BEST OCR RESULT ==========")
    print("Selected Method:", best_method)
    print("Best Accuracy:", scores[best_method], "%")

    print("\n========== FINAL EXTRACTED TEXT ==========")
    print(best_text)

    # Step 13: Extract individual fields from best OCR result

    extracted_fields = extract_fields(best_text)

    print("\n========== STRUCTURED LABEL DATA ==========")

    for field, value in extracted_fields.items():
        print(field + ":", value)

    # Step 14: Verify extracted label fields

    validation_results = validate_label(extracted_fields)

    print("\n========== FINAL LABEL VERIFICATION ==========")

    for field, status in validation_results.items():
        print(field + ":", status)