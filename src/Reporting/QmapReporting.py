import csv


def find_most_frequent_id(beads, th=750):
    """
    Find the most frequent ID among the beads whose brightness exceeds a given threshold.

    :param beads: A dictionary of bead data.
    :param th: Threshold for brightness. Only beads with brightness greater than this value are considered.
    :return: The most frequent ID.
    """
    # Filter beads that have brightness over the threshold and a non-None ID
    filtered_beads = [bead for bead in beads.values() if
                      bead['brightness'] is not None and bead['brightness'] > th and bead['ID'] is not None]

    # Count the occurrence of each ID
    id_counts = {}
    for bead in filtered_beads:
        id_counts[bead['ID']] = id_counts.get(bead['ID'], 0) + 1

    # Find the ID with the maximum occurrence
    most_frequent_id = None
    max_count = 0
    for id, count in id_counts.items():
        if count > max_count:
            most_frequent_id = id
            max_count = count

    return most_frequent_id


def qmap_reporting(beads, _dst):
    """
    Generate a CSV report of beads data and print the most frequent ID.

    :param beads: A dictionary of bead data.
    :param _dst: Destination path for the CSV file.
    """
    # Save the bead data to a CSV file
    csv_file = _dst + "/report.csv"
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['ID', 'x', 'y', 'r', 'brightness', 'ID'])

        # Write each bead's data as a row in the CSV
        for bead_id, bead_data in beads.items():
            writer.writerow([bead_id] + list(bead_data.values()))

    # Find the most frequent ID and print it
    most_frequent_id = find_most_frequent_id(beads)
    print(f"QmapID - {most_frequent_id}")
