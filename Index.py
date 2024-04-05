import cv2
import numpy as np


def remove_white_background(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary mask of the white background
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # Create a transparent background (RGBA)
    h, w, _ = image.shape
    transparent_image = np.zeros((h, w, 4), dtype=np.uint8)

    # Replace the white background with the transparent background
    transparent_image[:, :, :3] = masked_image  # Copy BGR channels
    transparent_image[:, :, 3] = 255  # Set the alpha channel to fully opaque

    # Save the output image
    cv2.imwrite("output.png", transparent_image)


# Call the function with the path to your image
remove_white_background("input.png")
