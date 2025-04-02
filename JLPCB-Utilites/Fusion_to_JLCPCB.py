import csv
import os
import re

# Function to convert BOM files
def convert_bom(input_file, output_file):
    # Define the new header
    header = ["Comment", "Designator", "Footprint", "LCSC Part number"]
    
    # Regular expression to match the pattern "C" followed by 3 to 10 digits
    lcsc_pattern = re.compile(r"^C\d{3,10}$")
    
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Skip the original header
        next(reader)
        
        # Write the new header
        writer.writerow(header)
        
        # Process and write the rows
        for row in reader:
            value = row[1]        # Value
            designator = row[0]   # Part
            footprint = row[3]    # Package
            lcsc_part = row[4]    # Description
            
            # Check if the LCSC Part number matches the pattern
            if not lcsc_pattern.match(lcsc_part):
                lcsc_part = "C00000"  # Replace with "C00000" if it doesn't match
            
            # Write the transformed row
            writer.writerow([value, designator, footprint, lcsc_part])

# Function to convert CPL files
def convert_cpl(input_file, layer):
    rows = []
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        # Skip the original header
        next(reader)
        # Process and collect the rows
        for row in reader:
            designator = row[0]  # Name
            mid_x = row[1]       # X
            mid_y = row[2]       # Y
            rotation = row[3]    # Angle
            rows.append([designator, mid_x, mid_y, layer, rotation])
    return rows

# Function to process all files in the directory
def process_directory(directory, bom_output_file, cpl_output_file):
    # Process BOM files
    for filename in os.listdir(directory):
        if filename.startswith("FUSION_BOM_") and filename.endswith(".csv"):
            input_file = os.path.join(directory, filename)
            print(f"Processing BOM file: {input_file}")
            convert_bom(input_file, bom_output_file)
            print(f"Converted BOM file saved as: {bom_output_file}")
    
    # Process CPL files
    header = ["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]
    all_rows = []
    for filename in os.listdir(directory):
        if filename.startswith("FUSION_CPL_") and filename.endswith(".csv"):
            # Determine the layer based on the filename
            if filename.endswith("_front.csv"):
                layer = "Top"
            elif filename.endswith("_back.csv"):
                layer = "Bottom"
            else:
                print(f"Skipping CPL file {filename}: Unable to determine layer.")
                continue
            
            input_file = os.path.join(directory, filename)
            print(f"Processing CPL file: {input_file}")
            rows = convert_cpl(input_file, layer)
            all_rows.extend(rows)
            print(f"Processed CPL file: {input_file}")
    
    # Write all combined CPL rows to the output file
    with open(cpl_output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header
        writer.writerows(all_rows)  # Write all rows
    print(f"Combined CPL output saved as: {cpl_output_file}")

# Example usage:
directory_path = os.path.dirname(os.path.abspath(__file__))  # Use the directory where the script is being run
bom_output_path = os.path.join(directory_path, "JLPCB_BOM_files.csv")  # Use directory_path for BOM output file path
cpl_output_path = os.path.join(directory_path, "JLPCB_CPL_files.csv")  # Use directory_path for CPL output file path
process_directory(directory_path, bom_output_path, cpl_output_path)