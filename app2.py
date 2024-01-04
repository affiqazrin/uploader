from flask import Flask, request, render_template, redirect, url_for, session, flash

# ... (your existing code)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Clear cache, memory, and session when re-uploading new files
    global decrypted_workbook, data, sql_query
    decrypted_workbook = io.BytesIO()
    data = {}
    sql_query = None
    session.clear()

    df = {}
    lst_sheet = []
    worksheet_names = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", 'error')
            return redirect(url_for('index'))

        file = request.files['file']
        print(file)
        if file.filename == '':
            flash("No selected file", 'error')
            return redirect(url_for('index'))

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df, lst_sheet, f = processor.read_insx_file(filepath, decrypted_workbook)
                print(lst_sheet)
                session['f'] = f

            except Exception as e:
                flash(f"An error occurred while reading the file: {str(e)}", 'error')
                return redirect(url_for('index'))

            return render_template('upload_single.html', worksheet_names=lst_sheet, uploaded_file=decrypted_workbook,
                                   categories=CATEGORIES, months=MONTHS)

    return render_template('upload_single.html', worksheet_names=lst_sheet, uploaded_file=None, categories=CATEGORIES, months=MONTHS)
