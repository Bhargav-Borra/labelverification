
import re


def extract_value(ocr_text, labels):

    # Join all possible field names into one regex pattern
    label_pattern = "|".join(
        re.escape(label) for label in labels
    )

    # Search for the field name at the beginning of a line
    pattern = (
        rf"^\s*(?:{label_pattern})"
        rf"\s*[:\-]?\s*(.*?)\s*$"
    )

    match = re.search(
        pattern,
        ocr_text,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        value = match.group(1).strip()
        return value if value else None

    return None


def extract_fields(ocr_text):

    # Extract Product Name
    product_name = extract_value(
        ocr_text,
        ["PRODUCT NAME", "BRAND NAME", "PRODUCT"]
    )

    # Extract Batch Number
    batch_number = extract_value(
        ocr_text,
        [
            "BATCH NUMBER",
            "BATCH NO",
            "LOT NUMBER",
            "LOT NO",
            "BATCH",
            "LOT"
        ]
    )

    # Extract Manufacturing Date
    mfg_date = extract_value(
        ocr_text,
        [
            "DATE OF MANUFACTURE",
            "MANUFACTURING DATE",
            "MANUFACTURED ON",
            "MFG DATE",
            "MFD",
            "MFG"
        ]
    )

    # Extract Expiry Date
    exp_date = extract_value(
        ocr_text,
        [
            "EXPIRATION DATE",
            "EXPIRY DATE",
            "EXP DATE",
            "USE BEFORE",
            "USE BY",
            "BEST BEFORE",
            "EXP"
        ]
    )

    # Extract MRP
    mrp = extract_value(
        ocr_text,
        ["MAXIMUM RETAIL PRICE", "MRP"]
    )

    # Return all extracted fields
    extracted_fields = {
        "Product Name": product_name,
        "Batch Number": batch_number,
        "Manufacturing Date": mfg_date,
        "Expiry Date": exp_date,
        "MRP": mrp
    }

    return extracted_fields


# Testing with different label formats
if __name__ == "__main__":

    test_labels = [

        # Test 1: Original format
        """
        PRODUCT NAME: TEST WHISKY
        BATCH NO: B12345
        MFG DATE: 1-10-2026
        EXP DATE: 1-10-2028
        MRP: 750
        """,

        # Test 2: Different field names
        """
        PRODUCT: COOKING OIL
        LOT NUMBER: XY9876
        MANUFACTURED ON: 15-08-2026
        USE BY: 15-08-2027
        MAXIMUM RETAIL PRICE: 180
        """,

        # Test 3: Another label format
        """
        BRAND NAME: FACE WASH
        BATCH: AB456
        MFD: 10-09-2026
        BEST BEFORE: 10-09-2028
        MRP: 250
        """
    ]

    for i, ocr_text in enumerate(test_labels, start=1):

        print(f"\n========== TEST {i} ==========")

        result = extract_fields(ocr_text)

        for field, value in result.items():
            print(field + ":", value)
