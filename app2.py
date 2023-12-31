@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    lst_sheet = []
    worksheet_names = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        files = request.files.getlist('file')  # Handle multiple files

        for file in files:
            if file.filename == '':
                return "No selected file"

            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                try:
                    # Process the uploaded file
                    df, lst_sheet, f = processor.read_insx_file(filepath, decrypted_workbook)
                    print(lst_sheet)
                    session['f'] = f

                    # Clear browser cache and cookies
                    response = make_response(render_template('upload_single.html', worksheet_names=lst_sheet,
                                                             uploaded_file=decrypted_workbook,
                                                             categories=CATEGORIES, months=MONTHS))
                    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
                    response.headers['Pragma'] = 'no-cache'
                    response.headers['Set-Cookie'] = 'name=value; max-age=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'

                    return response

                except Exception as e:
                    return f"An error occurred while reading the file: {str(e)}"

    return render_template('upload_single.html', worksheet_names=lst_sheet, uploaded_file=None,
                           categories=CATEGORIES, months=MONTHS)
