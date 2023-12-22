try:
    xl = pd.ExcelFile(exported_file_path)
    sheet_names = [sheet for sheet in xl.sheet_names]
    #uncomment to view list of worksheets
    #print(list(sheet_names))
    print(os.path.basename(f))
    print()            
except Exception as a:
    print("File cannot open with error: ", a)


    
        File cannot open with error:  expected <class 'datetime.datetime'>
