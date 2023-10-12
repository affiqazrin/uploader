from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import os
from openpyxl import load_workbook

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
allowed_extensions = {'xlsx', 'xls'}

# Function to get Excel sheet names
def get_excel_sheet_names(file_path):
    workbook = load_workbook(file_path, read_only=True, data_only=True)
    sheet_names = workbook.sheetnames
    return sheet_names

# Function to check if a file has allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Sample ETL function (modify as needed)
def perform_etl(file_path, worksheet_name, header_row):
    df = pd.read_excel(file_path, sheet_name=worksheet_name, header=header_row)
    # Implement your ETL logic here
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    worksheet_names = None  # Initialize worksheet_names

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']

        if file.filename == '':
            return "No selected file"
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                workbook = pd.ExcelFile(filepath)
                worksheet_names = workbook.sheet_names
            except Exception as e:
                return f"An error occurred while reading the file: {str(e)}"

            return render_template('upload_single.html', worksheet_names=worksheet_names, uploaded_file=filename)

    return render_template('upload_single.html', worksheet_names=worksheet_names, uploaded_file=None)

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    worksheet_name = request.form['worksheet']
    uploaded_file = request.form['uploaded_file']

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file)
        df = pd.read_excel(filepath, sheet_name=worksheet_name)

        # Debugging statements
        print(f"Worksheet name: {worksheet_name}")
        print(f"Uploaded file: {uploaded_file}")

        # Convert the DataFrame to an HTML table
        html_table = df.to_html(classes="table table-striped")

        return html_table

    except Exception as e:
        error_message = f"An error occurred while reading the worksheet: {str(e)}"
        return error_message, 500  # Return a 500 Internal Server Error status code
        
        
@app.route('/list', methods=['GET', 'POST'])
def etl_job():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(debug=True)