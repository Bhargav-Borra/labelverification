
import os
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from verification import verify_label_image

# Step 1: Create Flask application
app = Flask(__name__)
CORS(app)

# Step 2: Configure upload folder
UPLOAD_FOLDER = os.path.join(
    tempfile.gettempdir(),
    "excise_label_uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Step 3: Allowed image formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}


# Step 4: Check image file extension
def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Step 5: Homepage route
@app.route("/")
def home():

    return "Excise Label Verification System API is Running!"


# Step 6: Image upload API
@app.route("/upload", methods=["POST"])
def upload_image():

    # Check whether an image was uploaded
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Check whether a filename exists
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Check whether the file format is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid image format"}), 400

    # Secure the filename
    filename = secure_filename(file.filename)

    # Save the uploaded image
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(file_path)

    # Step 8: Verify the uploaded image
    result = verify_label_image(file_path)

    if "error" in result:
        return jsonify(result), 400

    # Step 9: Return verification results
    return jsonify({
        "message": "Image uploaded and verified successfully",
        "filename": filename,
        **result
    }), 200


# Step 7: Run Flask application
if __name__ == "__main__":

    app.run(debug=True)
