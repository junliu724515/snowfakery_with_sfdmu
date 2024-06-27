"""
Step 1: Reading CSV Files from csvw_metadata.json:
    First, parse the csvw_metadata.json file to extract the list of CSV files you want to process. You can use Python’s built-in json module to read the JSON data and retrieve the file names.
    Looping Through CSV Files:

Step 2:Iterate through each CSV file in the list obtained from step 1.
    For each CSV file:
        Read the file content (e.g., using Python’s csv module).
        Replace the header value “id” with “Id” (case-insensitive) in the first row of the CSV file.

Step 3: Creating the sfdmu export.json:
    Assemble the modified CSV data into the desired format for SFDU. Typically, this involves creating a JSON file (e.g., export.json) that follows the SFDU format.
    Each record in the JSON file corresponds to a record in Salesforce, with field names (including “Id”) as keys and corresponding values.
"""

import os
import csv
import json
import argparse

def process_csv_file(folder, csv_file):
    """
    Process a single CSV file.

    This function reads a CSV file, modifies the header row to replace "id" with "Id",
    writes the modified CSV data back to the file, and constructs a dictionary object
    representing a query for the CSV data.

    Args:
        folder (str): The directory containing the CSV file.
        csv_file (str): The name of the CSV file.

    Returns:
        dict: A dictionary object representing a query for the CSV data, or None if an error occurs.
    """
    file_path = os.path.join(folder, csv_file)
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found in {folder}")
        return None

    if not rows:
        print(f"Error: File {csv_file} is empty")
        return None

    # Update header row
    rows[0] = ['Id' if cell.lower() == 'id' else cell for cell in rows[0]]

    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except IOError as e:
        print(f"Error writing to file {csv_file}: {e}")
        return None

    obj = {
        "query": f"SELECT Id, {', '.join(rows[0])} FROM {os.path.splitext(csv_file)[0]}",
        "operation": "Insert",
        "externalId": "Id"
    }
    return obj

def process_csv_files(folder, csv_files):
    """
    Process a list of CSV files.

    This function processes each CSV file in the list by calling process_csv_file().

    Args:
        folder (str): The directory containing the CSV files.
        csv_files (list): A list of CSV file names.

    Returns:
        list: A list of dictionary objects representing queries for the CSV data.
    """
    objects = []
    for csv_file in csv_files:
        obj = process_csv_file(folder, csv_file)
        if obj:
            objects.append(obj)
    return objects

def generate_export_json(output_folder):
    """
    Generate an export.json file.

    This function reads a csvw_metadata.json file to get a list of CSV files,
    processes each CSV file by calling process_csv_files(), and writes the resulting
    list of dictionary objects to an export.json file.

    Args:
        output_folder (str): The directory containing the csvw_metadata.json file and where the export.json file will be written.
    """
    metadata_path = os.path.join(output_folder, 'csvw_metadata.json')
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
    except FileNotFoundError:
        print(f"Error: SnowFakery Metadata file not found in {output_folder}")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode SnowFakery JSON from {metadata_path}")
        return

    csv_files = [table['url'] for table in metadata.get('tables', [])]
    objects = process_csv_files(output_folder, csv_files)

    export_path = os.path.join(output_folder, 'export.json')
    try:
        with open(export_path, 'w') as file:
            json.dump({"objects": objects}, file, indent=4)
    except IOError as e:
        print(f"Error writing to export.json: {e}")

def main():
    """
    Main function.

    This function parses command-line arguments and calls generate_export_json() with the specified SnowFakery folder.
    """
    parser = argparse.ArgumentParser(description='Process CSV files and produce a JSON file.')
    parser.add_argument('SnowFakeryFolder', metavar='snowfakeryfolder', type=str, help='the path to the SnowFakery folder')
    args = parser.parse_args()

    generate_export_json(args.SnowFakeryFolder)

if __name__ == "__main__":
    main()