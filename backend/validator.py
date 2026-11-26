
from datetime import datetime

# Supported date formats
DATE_FORMATS = [
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d.%m.%Y",
    "%Y-%m-%d"
]


# Step 1: Convert date string into a date object

def parse_date(date_string):

    if date_string is None:
        return None

    date_string = date_string.strip()

    for date_format in DATE_FORMATS:

        try:
            return datetime.strptime(date_string, date_format)

        except ValueError:
            continue

    return None


# Step 2: Validate Product Name

def validate_product_name(product_name):

    if product_name is None or product_name.strip() == "":
        return False

    return True


# Step 3: Validate Batch Number

def validate_batch_number(batch_number):

    if batch_number is None or batch_number.strip() == "":
        return False

    return True


# Step 4: Validate Manufacturing Date

def validate_mfg_date(mfg_date):

    manufacturing_date = parse_date(mfg_date)

    return manufacturing_date is not None


# Step 5: Validate Expiry Date

def validate_expiry_date(mfg_date, exp_date):

    manufacturing_date = parse_date(mfg_date)
    expiry_date = parse_date(exp_date)

    if manufacturing_date is None or expiry_date is None:
        return False

    return expiry_date > manufacturing_date


# Step 6: Validate MRP

def validate_mrp(mrp):

    if mrp is None:
        return False

    try:
        mrp = float(mrp)

        if mrp > 0:
            return True

        return False

    except ValueError:
        return False


# Step 7: Validate Complete Label

def validate_label(fields):

    validation_results = {

        "Product Name": validate_product_name(
            fields.get("Product Name")
        ),

        "Batch Number": validate_batch_number(
            fields.get("Batch Number")
        ),

        "Manufacturing Date": validate_mfg_date(
            fields.get("Manufacturing Date")
        ),

        "Expiry Date": validate_expiry_date(
            fields.get("Manufacturing Date"),
            fields.get("Expiry Date")
        ),

        "MRP": validate_mrp(
            fields.get("MRP")
        )
    }

    if all(validation_results.values()):
        label_status = "VALID"
    else:
        label_status = "INVALID"

    validation_results["Label Status"] = label_status

    return validation_results


# Testing

if __name__ == "__main__":

    label_data = {
        "Product Name": "TEST WHISKY",
        "Batch Number": "B12345",
        "Manufacturing Date": "01-10-2026",
        "Expiry Date": "01-10-2028",
        "MRP": "750"
    }

    result = validate_label(label_data)

    print("\n========== FINAL VERIFICATION ==========")

    for field, status in result.items():
        print(field + ":", status)
