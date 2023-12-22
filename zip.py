import os
import zipfile as zf
import glob

def extract_zip_file(password, input_file_path, INFILE):
    
    output_directory=os.path.dirname(input_file_path)

    input_file_name=os.path.basename(input_file_path)
    
    output_file_name=input_file_name.replace('zip', 'xlsx')

    try:
        with zf.ZipFile(input_file_path, 'r') as zip_ref:
            if password:
                zip_ref.setpassword(password.encode('utf-8'))

            zip_ref.extractall(output_directory)
        print(f"Extracting {output_file_name}")

        return os.path.join(INFILE, output_file_name)

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

    
password='VrK3@*12'
input_file_path = os.path.join(SRC, file_select.value)
exported_file_path = extract_zip_file(password, input_file_path, INFILE)

if exported_file_path:
    print(f"Running {exported_file_path}")
