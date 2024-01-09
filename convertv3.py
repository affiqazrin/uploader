#convert value column to float data type
convert_lst=['RP', 'rp' 'RM', 'rm', 'CC', 'cc', 'tgt', 'ach', 'act', 'rate', 'payout', 'ye_rate', 'amt', 'amount', 'deduct', 'rem1','rem2', 'rem3', 'rem4', 'total', 'rm', 'ret', 'oth_clw', 'cf_clw']

for i in range(len(convert_lst)):
    #print(convert_lst[i])
    for cols in df_ws4.columns:
        if convert_lst[i] in cols:
            df_ws4[cols]=df_ws4[cols].astype(float)
            
df_ws4.dtypes
