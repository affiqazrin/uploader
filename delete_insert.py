#delete
try:
    DELETE_RECORD=pd.read_sql_query("DELETE FROM "+params['to_temp_table']+" WHERE Month="+f"'"{params['Month']}', engine)
except:
    print('Records: '+f'{params['Month']}'+' deleted successfully')
    #df=pd.read_sql("SELECT * FROM "+params[params_list[1]]+" WHERE Month=%(month)s LIMIT 10", engine)
#df

#insert
try:
    d['Sheet1'][list(rename_cols.values())].to_sql(con=engine, name=params['to_temp_table'], if_exists='replace', index=False)
    print(d['Sheet1'][list(rename_cols.values())].columns)
    print(d['Sheet1'][list(rename_cols.values())].shape)
except:
    print("OE: ", e)
    print("Error Code: ", e.orig.args[0]) 
