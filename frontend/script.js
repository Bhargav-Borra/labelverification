
// ==========================================
// STEP 1: GET HTML ELEMENTS
// ==========================================

const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.querySelector(".preview-container");
const verifyButton = document.getElementById("verifyButton");

// Verification result elements
const resultsContainer = document.getElementById("resultsContainer");
const verificationStatus = document.getElementById("verificationStatus");
const resultDetails = document.getElementById("resultDetails");

// Store previous preview URL
let previewURL = null;


// ==========================================
// STEP 2: HANDLE IMAGE SELECTION
// ==========================================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    console.log("Selected image:", file);

    if (!file) {
        previewContainer.style.display = "none";
        return;
    }

    // Check allowed extensions
    const allowedExtensions = ["png", "jpg", "jpeg", "bmp"];

    const fileExtension = file.name
        .split(".")
        .pop()
        .toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {

        alert("Please select PNG, JPG, JPEG or BMP image.");

        imageInput.value = "";
        previewContainer.style.display = "none";

        return;
    }

    // Remove previous preview URL
    if (previewURL !== null) {
        URL.revokeObjectURL(previewURL);
    }

    // Create temporary image URL
    previewURL = URL.createObjectURL(file);

    imagePreview.onload = function () {

        previewContainer.style.display = "block";

        console.log("Image preview loaded successfully!");

    };

    imagePreview.onerror = function () {

        previewContainer.style.display = "none";

        alert("Unable to preview this image.");

        URL.revokeObjectURL(previewURL);

        previewURL = null;

    };

    imagePreview.src = previewURL;

});



// ==========================================
// STEP 3: DISPLAY VERIFICATION RESULTS
// ==========================================

function displayResults(result) {

    // Get final verification status
    const status = result.validation["Label Status"];

    // Show results container
    resultsContainer.style.display = "block";

    // Display VALID or INVALID
    verificationStatus.textContent = "Label Status: " + status;

    // Apply status styling
    verificationStatus.className =
        status === "VALID" ? "valid-status" : "invalid-status";

    // Get extracted fields
    const fields = result.extracted_fields;

    // Get individual validation results
    const validation = result.validation;

    // Fields to display
    const fieldNames = [
        "Product Name",
        "Batch Number",
        "Manufacturing Date",
        "Expiry Date",
        "MRP"
    ];

    // Clear previous results
    resultDetails.innerHTML = "";

    // Display extracted field values
    fieldNames.forEach(function (field) {

        const row = document.createElement("div");
        row.className = "result-row";

        const label = document.createElement("strong");
        label.textContent = field;

        const value = document.createElement("span");
        value.textContent = fields[field] || "Not detected";

        row.appendChild(label);
        row.appendChild(value);

        resultDetails.appendChild(row);

    });

    // Create validation heading
    const validationHeading = document.createElement("h3");
    validationHeading.textContent = "Individual Field Validation";

    resultDetails.appendChild(validationHeading);

    // Display individual validation results
    fieldNames.forEach(function (field) {

        const row = document.createElement("div");
        row.className = "result-row";

        const label = document.createElement("strong");
        label.textContent = field;

        const value = document.createElement("span");

        if (validation[field] === true) {

            value.textContent = "✓ PASS";
            value.className = "validation-pass";

        } else {

            value.textContent = "✗ FAIL";
            value.className = "validation-fail";

        }

        row.appendChild(label);
        row.appendChild(value);

        resultDetails.appendChild(row);

    });

    // Display OCR information
    const ocrInfo = document.createElement("p");

    ocrInfo.textContent =
        "Selected OCR Method: " + result.selected_method +
        " | Detected Fields: " + result.detected_field_count;

    resultDetails.appendChild(ocrInfo);

}


// ==========================================
// STEP 4: HANDLE VERIFY BUTTON CLICK
// ==========================================

verifyButton.addEventListener("click", async function (event) {

    // Prevent default browser action
    event.preventDefault();

    console.log("VERIFY BUTTON CLICKED!");

    const file = imageInput.files[0];

    // Check whether image is selected
    if (!file) {

        alert("Please select an image first.");

        return;

    }

    // Prepare image for uploading
    const formData = new FormData();

    formData.append("image", file);

    try {

        // Show loading status
        verifyButton.disabled = true;

        verifyButton.textContent = "Verifying...";

        console.log("Sending image to Flask backend...");

        // Send image to Flask API
        const response = await fetch(
            "http://127.0.0.1:5000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        // Read backend response
        const result = await response.json();

        console.log("HTTP Status:", response.status);

        console.log("Verification Result:", result);

        // Check backend response
        if (!response.ok) {

            alert(
                "Verification failed: " +
                (result.error || "Unknown error")
            );

            return;

        }

        // Display verification results on webpage
        displayResults(result);

    }

    catch (error) {

        console.error("Backend connection error:", error);

        alert(
            "Unable to connect to the backend. " +
            "Please check the Console for details."
        );

    }

    finally {

        // Restore button
        verifyButton.disabled = false;

        verifyButton.textContent = "Verify Label";

    }

});


// ==========================================
// STEP 5: CONFIRM JAVASCRIPT LOADED
// ==========================================

console.log(
    "Excise Label Verification System JavaScript loaded successfully!"
);
