import cv2
import numpy as np

def extract_bead_brightness(img_pe, beads):
    """
    Calculate the mean brightness of each detected bead in the provided image.

    :param img_pe: Path to the image file used for brightness extraction.
    :param beads: Dictionary containing information about the detected beads.
    """
    # Load the image in grayscale mode.
    image_gray = cv2.imread(img_pe, cv2.IMREAD_GRAYSCALE)

    # Iterate over all detected beads
    for iter in range(len(beads)):
        # Retrieve the center coordinates (x, y) and radius (r) of the current bead
        x, y, r = beads[iter]['x'], beads[iter]['y'], beads[iter]['r']

        # Create a circular mask for the current bead.
        # The mask is used to isolate the area of the bead in the image.
        mask = np.zeros_like(image_gray)
        cv2.circle(mask, (x, y), r - 1, 255, thickness=-1)

        # Calculate the mean brightness value inside the circle defined by the mask.
        # cv2.mean returns a tuple, where the first element is the mean value of the pixels under the mask.
        mean_val = cv2.mean(image_gray, mask=mask)[0]

        # Update the 'brightness' field for the current bead in the dictionary.
        # The brightness value is scaled by multiplying it by 140 for calibration purposes.
        beads[iter]['brightness'] = mean_val * 140
