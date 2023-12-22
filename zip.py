zip_file=os.path.join(INFILE, file_select.value)
zip_file_name = os.path.basename(zip_file)

print(zip_file)
print()
print(zip_file_name)

pwd='AML@2023'

with zf.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.setpassword(pwd.encode('utf-8'))
    zip_ref.extractall(INFILE)

xls_file_name = zip_file_name.replace('zip','xlsx')
print(f"Extracting {xls_file_name}")

today_file = glob.glob(os.path.join(INFILE, xls_file_name))[0]
print(f"Running {today_file}")
