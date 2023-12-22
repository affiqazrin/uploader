import os
import zipfile as zf
import glob

def extract_zip_file(password, input_file_path):
    # Construct the output directory
    output_directory = os.path.dirname(input_file_path)

    # Get the base name of the input file
    input_file_name = os.path.basename(input_file_path)

    # Construct the output file name
    output_file_name = input_file_name.replace('zip', 'xlsx')

    # Construct the output file path
    output_file_path = os.path.join(output_directory, output_file_name)

    try:
        # Open the ZIP file
        with zf.ZipFile(input_file_path, 'r') as zip_ref:
            # Set the password (if provided)
            if password:
                zip_ref.setpassword(password.encode('utf-8'))

            # Extract all contents to the output directory
            zip_ref.extractall(output_directory)

        # Print information about the extracted file
        print(f"Extracting {output_file_name}")

        # Return the path of the extracted file
        return os.path.join(output_directory, output_file_name)

    except zf.BadZipFile:
        # Handle the case where the file is not a valid ZIP file
        print("Error: The provided file is not a valid ZIP file.")
        return None

    except zf.LargeZipFile:
        # Handle the case where the ZIP file is too large to handle
        print("Error: The ZIP file is too large to handle.")
        return None

    except zf.BadPassword:
        # Handle the case where the provided password is incorrect
        print("Error: Incorrect password for the ZIP file.")
        return None

# Example usage:
password = 'AML@2023'
input_file_path = os.path.join(INFILE, file_select.value)
exported_file_path = extract_zip_file(password, input_file_path)

if exported_file_path:
    print(f"Running {exported_file_path}")
    # Add your further processing code here, if needed
