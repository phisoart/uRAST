import cv2
import numpy as np
from ..helper import jsonHelper

def find_nearest_blob_center(centroids, image_center):
    """
    Calculate the distances from the image center to each blob center and return the index of the nearest center.
    If the nearest center is more than 5 units away, return -1 to indicate no suitable center was found.
    """
    distances = np.sqrt([(center[0] - image_center[0]) ** 2 +
                         (center[1] - image_center[1]) ** 2 for center in centroids])
    if np.argmin(distances) > 5:
        return -1
    return np.argmin(distances)

def is_angle_similar(angle1, angle2, tolerance=50):
    """Check if two angles are within a given tolerance."""
    return abs(angle1 - angle2) <= tolerance or abs((angle1 - angle2) % 360) <= tolerance

def analyid(_info, _angles, _distance):
    """
    Analyze if the given angles and distances match the provided qmap information.
    """
    if _info["n"] != len(_angles) or _info["n"] != len(_distance):
        return False
    angles1 = _info["angle_array"]
    distances1 = _info["distance_array"]
    angles2 = _angles
    distances2 = _distance

    # Rotation and reflection check
    for i in range(len(angles1)):
        # Rotation
        rotated_angles = angles1[i:] + angles1[:i]
        rotated_distances = distances1[i:] + distances1[:i]

        if all(is_angle_similar(a1, a2) for a1, a2 in zip(rotated_angles, angles2)) and rotated_distances == distances2:
            return True

        # Reflection and then rotation
        reflected_angles = angles1[::-1]
        reflected_distances = distances1[::-1]
        reflected_rotated_angles = reflected_angles[i:] + reflected_angles[:i]
        reflected_rotated_distances = reflected_distances[i:] + reflected_distances[:i]

        if all(is_angle_similar(a1, a2) for a1, a2 in zip(reflected_rotated_angles, angles2)) and reflected_rotated_distances == distances2:
            return True

    return False

def sort_and_filter_lists(_angles, _distances):
    """
    Sort and filter the angles and distances lists.
    Angles are sorted and distances are adjusted accordingly.
    Filter out angles with small differences and adjust distances based on specific conditions.
    """
    # Sort angles and distances
    sorted_indices = np.argsort(_angles)
    sorted_angles = np.array(_angles)[sorted_indices]
    sorted_distances = np.array(_distances)[sorted_indices]

    # Initialize result lists
    filtered_angles = []
    filtered_distances = []

    # Iterate and filter based on angle differences and distance conditions
    i = 0
    while i < len(sorted_angles) - 1:
        angle_difference = abs(sorted_angles[i] - sorted_angles[i + 1])
        # Check if angles are within 5 degrees or their circular equivalent
        if angle_difference <= 5 or abs(angle_difference - 360) <= 5 or abs(angle_difference + 360) <= 5:
            # Check distance conditions
            if (7.5 <= sorted_distances[i] <= 10 and 12 <= sorted_distances[i + 1] <= 15) or \
                    (7.5 <= sorted_distances[i + 1] <= 10 and 12 <= sorted_distances[i] <= 15):
                filtered_angles.append(sorted_angles[i])
                filtered_distances.append(0)
                i += 2
                continue
        # Store distance condition as 1 or 2 based on range
        if 7.5 <= sorted_distances[i] <= 10:
            filtered_angles.append(sorted_angles[i])
            filtered_distances.append(1)
            i += 1
        elif 12 <= sorted_distances[i] <= 14:
            filtered_angles.append(sorted_angles[i])
            filtered_distances.append(2)
            i += 1
        else:
            i += 1
            continue

    # Process the last element
    if i == len(sorted_angles) - 1:
        angle_difference = abs(sorted_angles[i] - sorted_angles[0])
        filtered_angles.append(sorted_angles[i])
        if 7.5 <= sorted_distances[i] <= 10:
            filtered_distances.append(1)
        elif 12 <= sorted_distances[i] <= 14:
            filtered_distances.append(2)
        else:
            filtered_distances.append(sorted_distances[i])

    # Adjust angles to be differences with the next element
    for iter, _filtered_angle in enumerate(filtered_angles):
        last = abs(filtered_angles[0] - filtered_angles[len(filtered_angles) - 1])
        if last > 360:
            last -= 360
        filtered_angles[iter] = abs(filtered_angles[iter + 1] - _filtered_angle) if iter < len(filtered_angles) - 1 else last

    return filtered_angles, filtered_distances

def bead_decoding(img_bf, beads, _dst):
    """
    Process each detected bead in the image. For each bead, apply binary thresholding,
    find the connected components, and calculate angles and distances.
    Save relevant images for each bead and assign an ID based on qmap analysis.
    """
    # Convert the image to grayscale
    image_gray = cv2.imread(img_bf, cv2.IMREAD_GRAYSCALE)
    qmap_info = jsonHelper.load_json_file("res/config/qmap_info.json")

    # Process each detected bead
    for iter, bead in enumerate(beads.values()):
        # Get center coordinates and radius of the bead
        x, y, r = int(bead['x']), int(bead['y']), int(bead['r'])
        # Create a mask for the bead
        mask = np.zeros_like(image_gray)
        cv2.circle(mask, (x, y), r + 1, 255, thickness=-1)

        # Crop the bead from the image using the mask
        circle_image = cv2.bitwise_and(image_gray, image_gray, mask=mask)
        circle_image = circle_image[y - r:y + r, x - r:x + r]

        if circle_image.size > 0:
            # Convert to grayscale and apply binary threshold
            gray = circle_image
            image_center = (gray.shape[1] // 2, gray.shape[0] // 2)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # Find connected components in the binary image
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, 8, cv2.CV_32S)
            if len(centroids) < 7 or len(centroids) > 10:
                continue
            # Find the nearest blob center to the image center
            nearest_blob_index = find_nearest_blob_center(centroids[1:], image_center) + 1
            if nearest_blob_index == -1:
                continue
            central_blob_center = centroids[nearest_blob_index]

            # Prepare the colored image for annotation
            colored_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            angles = []
            distances = []
            # Draw lines from the central blob to other blobs and calculate angles and distances
            for i in range(1, num_labels):
                if i == nearest_blob_index:
                    continue
                blob_center = tuple(np.round(centroids[i]).astype(int))
                distance = np.linalg.norm(centroids[i] - central_blob_center)

                if distance > 15 or distance < 7.5:
                    continue
                # Save images for the first bead as an example
                if iter == 0:
                    cv2.line(colored_image, tuple(np.round(central_blob_center).astype(int)), blob_center, (0, 0, 255),
                             2)
                    cv2.imwrite(_dst + f'/img{iter}_bead_crop.png', circle_image)
                    cv2.imwrite(_dst + f'/img{iter}_annotated_image.png', colored_image)
                    cv2.imwrite(_dst + f'/img{iter}_binary.png', binary)

                delta_x = blob_center[0] - central_blob_center[0]
                delta_y = blob_center[1] - central_blob_center[1]
                angle = np.arctan2(delta_y, delta_x)
                angle_degrees = np.degrees(angle)

                angles.append(angle_degrees)
                distances.append(distance)

            # Filter and sort angles and distances
            filtered_angles, filtered_distances = sort_and_filter_lists(angles, distances)
        for col in qmap_info:
            for id in qmap_info[col]:
                if analyid(id, filtered_angles, filtered_distances):
                    beads[iter]["ID"] = id["name"]
                    break
