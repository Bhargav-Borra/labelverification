
import cv2
import os


def preprocess_image(image):

    # Step 1: Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Resize image
    resized_image = cv2.resize(
        gray_image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Step 3: Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(
        resized_image,
        (5, 5),
        0
    )

    # Step 4: Apply normal thresholding
    _, threshold_image = cv2.threshold(
        blurred_image,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # Step 5: Apply adaptive thresholding
    adaptive_image = cv2.adaptiveThreshold(
        blurred_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Step 6: Return all processed images
    return {
        "grayscale": gray_image,
        "resized": resized_image,
        "blurred": blurred_image,
        "threshold": threshold_image,
        "adaptive": adaptive_image
    }



# Run this section only when this file is executed directly
if __name__ == "__main__":

    # Step 1: Read the image
    image = cv2.imread("dataset/raw_images/test_label.bmp")

    if image is None:
        print("Image not found!")

    else:
        # Step 2: Print original image shape
        print("Original Image Shape:", image.shape)

        # Step 3: Call preprocessing function
        processed_images = preprocess_image(image)

        print("Preprocessing completed successfully!")

        # Step 4: Print processed image names
        print("Processed Images:", processed_images.keys())

        # Step 5: Save all processed images automatically
        for name, processed_image in processed_images.items():

            file_path = os.path.join(
                "dataset/processed_images",
                name + "_label.png"
            )

            cv2.imwrite(file_path, processed_image)

            print(name, "image saved successfully!")
