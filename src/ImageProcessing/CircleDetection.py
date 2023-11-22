import cv2
import numpy as np

def circle_detection(img_bf, beads, _dst):
    """
    Detect circles in the provided image using Hough Circle Transform and update the beads dictionary.
    Also, save the result image with the detected circles drawn on it.

    :param img_bf: Path to the image file for circle detection.
    :param beads: Dictionary to store the detected circle information (x, y, radius).
    :param _dst: Destination directory to save the result image.
    """
    # Load the image file in grayscale mode.
    image = cv2.imread(img_bf, cv2.IMREAD_GRAYSCALE)

    # Detect circles in the image using OpenCV's HoughCircles function.
    circles = cv2.HoughCircles(image,
                               cv2.HOUGH_GRADIENT,  # Detection method
                               dp=1,                # Inverse ratio of the accumulator resolution
                               minDist=30,          # Minimum distance between the centers of detected circles
                               param1=50,           # Higher threshold for the internal Canny edge detector
                               param2=25,           # Threshold for center detection
                               minRadius=15,        # Minimum circle radius
                               maxRadius=22)        # Maximum circle radius

    # Check if any circles were found
    if circles is not None:
        # Convert the coordinates and radii to integers
        circles = np.round(circles[0, :]).astype("int")

        # Iterate through each detected circle
        for iter, (x, y, r) in enumerate(circles):
            # Update the beads dictionary with the circle's information
            beads[iter] = {"x": x, "y": y, "r": r, "brightness": None, "ID": None}
            # Draw the circle and its center point on the image for visual verification
            cv2.circle(image, (x, y), r, (255, 0, 0), 4)  # Circle
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)  # Center point

    # Save the image with the detected circles to the specified destination
    cv2.imwrite(_dst + '/circle_detection.png', image)
