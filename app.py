import io
import os
import openpyxl
import msoffcrypto
import pandas as pd
from random import randint, randrange

from openpyxl import load_workbook
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, text
from flask import Flask, request, render_template, redirect, url_for, session

from package import StatementProcessor

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='INC_STATEMENT'
app.config.from_object('config.ProductionConfig')  # Change to 'config.ProductionConfig' for production
app.config['_external_route_base'] = True

app.secret_key=str(randint(1, 9999999))
print(app.secret_key)


# Initialize the SQLAlchemy extension
db=SQLAlchemy(app)

MONTHS = [("January", "2301"), ("February", "2302"), ("March", "2303"), 
("April", "2304"), ("May", "2305"), ("June", "2306"), 
("July", "2307"), ("August", "2308"), ("September", "2309"), 
("October", "2310"), ("November", "2311"), ("December", "2312")]
CATEGORIES = [("Monthly", "1"), ("Quarterly", "Q")]



def create_db_engine():
    try:
        engine=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        print(engine)
        return engine

    except Exception as e:
        print(f"Error creating database engine: {str(e)}")
        return None
  
processor=StatementProcessor(create_db_engine())
decrypted_workbook=io.BytesIO()
data={}
sql_query=None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    df={}
    lst_sheet=[]
    worksheet_names=None
 
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file=request.files['file']
        print(file)
        if file.filename == '':
            return "No selected file"
        
        if file:
            filename=secure_filename(file.filename)
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)           
            try:
                df, lst_sheet, f=processor.read_insx_file(filepath, decrypted_workbook)
                print(lst_sheet)
                session['f']=f
                                    
            except Exception as e:
                return f"An error occurred while reading the file: {str(e)}"
                       
            return render_template('upload_single.html', worksheet_names=lst_sheet, uploaded_file=decrypted_workbook,
            categories=CATEGORIES, months=MONTHS)

    return render_template('upload_single.html', worksheet_names=lst_sheet, uploaded_file=None, categories=CATEGORIES, months=MONTHS)


@app.route('/fetch_data', methods=['POST'])
def fetch_data():

    session.clear()
    session['worksheet_name']=request.form['worksheet']
    session['uploaded_file']=request.form['uploaded_file']
    
    try:
        data=pd.read_excel(decrypted_workbook, session.get('worksheet_name'), engine='openpyxl')
        print(data.head(10))
        
        # Convert the DataFrame to an HTML table
        html_table=data.to_html(classes="table table-striped")       
        return html_table

    except Exception as e:
        error_message = f"An error occurred while reading the worksheet: {str(e)}"
        return error_message, 500


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

        data={}
        data=pd.read_excel(decrypted_workbook, session.get('worksheet_name'), engine='openpyxl')
        print(data.head(10))
        
        insg_to_insx=processor.read_insx_config(session.get('f'), session.get('selected_category'))        
        processed_data=processor.process_data(data, insg_to_insx, session.get('worksheet'), session.get('insx_cycle'), session.get('selected_month'))        
        #print(processed_data.head())
        
        html_table=processed_data.to_html(classes="table table-striped")    
        return html_table

    except Exception as e:
        error_message=f"An error occurred while processing the data: {str(e)}"
        return error_message, 500


@app.route('/append_to_db', methods=['POST'])
def append_to_db():
    try:
        processor.process_statement(session.get('f'), session.get('selected_category'), session.get('insx_cycle'), session.get('selected_month'))
        return "Data appended to database successfully"

    except Exception as e:
        error_message = f"An error occurred while appending data to the database: {str(e)}"
        return error_message, 500

             
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    engine=create_db_engine()
    print(engine)
    if engine is None:
        return "Error creating database engine", 500

    # Get the SQL query from the form    
    if request.method == 'POST':
        sql_query=request.form['query']
        print(sql_query)      
        try:
            # Fetch data from the MySQL database and convert it to a Pandas DataFrame
            with db.engine.begin() as conn:
                result=conn.execute(text(sql_query))
            df=pd.DataFrame(result)
        
            #df = pd.read_sql(sql_query, engine.raw_connection())
            #df=pd.DataFrame(engine.connect().execute(text(sql_query)))
            print(df.head(10))

            table_html=df.head(10).to_html(classes='table table-bordered', index=False)            
            return render_template('results.html', table=table_html)
            
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
            return "Error fetching data from the database", 500
            
    return render_template('results.html')

      
@app.route('/list', methods=['GET', 'POST'])
def etl_job():
    return render_template('list.html')




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8888)
