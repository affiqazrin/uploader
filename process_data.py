@app.route('/process_data', methods=['POST'])
def process_data():
    session['selected_category']=request.form['category']
    session['selected_month']=request.form['month']

    sql_query=f"""
        SELECT 
            CASE 
                WHEN SUBSTRING(input_date, 3, 2) BETWEEN '01' AND '03' THEN 'Q4'
                WHEN SUBSTRING(input_date, 3, 2) BETWEEN '04' AND '06' THEN 'Q1'
                WHEN SUBSTRING(input_date, 3, 2) BETWEEN '07' AND '09' THEN 'Q2'
                WHEN SUBSTRING(input_date, 3, 2) BETWEEN '10' AND '12' THEN 'Q3'
                ELSE NULL
            END AS fiscal_quarter
        FROM (SELECT {session.get('selected_month')} AS input_date) AS input_date_subquery;
    """
    input_date_value=session.get('selected_month')
    try:
        with db.engine.begin() as conn:
            result=conn.execute(text(sql_query))
            
        temp=pd.DataFrame(result, columns=result.keys())
        session['insx_cycle']=str(temp['fiscal_quarter'].iloc[0])

    except Exception as e:
        print(f"Error fetching data from the database: {str(e)}")
        return "Error fetching data from the database", 500

    try:        
        insx_file_name=os.path.basename(session.get('f')).split('.')[0]
        #print(insx_file_name)
        
        if session.get('f') is None:
            return "Data not found", 404

        #data={}
        data=pd.read_excel(decrypted_workbook, session.get('worksheet_name'), engine='openpyxl').copy()
        print(data.head(10))
        
        insg_to_insx=processor.read_insx_config(session.get('f'), session.get('selected_category'))        
        processed_data=processor.process_data(data, insg_to_insx, session.get('worksheet'), session.get('insx_cycle'), session.get('selected_month'))        
        html_table=processed_data.to_html(classes="table table-striped")    
        return html_table

    except Exception as e:
        error_message=f"An error occurred while processing the data: {str(e)}"
        return error_message, 500
