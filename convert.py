        # Convert value column to float data type
        convert_lst = ['RP', 'rp', 'RM', 'rm', 'CC', 'cc', 'tgt', 'ach', 'act', 'rate', 'payout',
                       'ye_rate', 'amt', 'amount', 'deduct', 'rem1', 'rem2', 'rem3', 'rem4', 'total',
                       'rm', 'ret', 'oth_clw', 'cf_clw']

        for col in df_filtered.columns:
            for convert_item in convert_lst:
                if convert_item in col:
                    try:
                        df_filtered.loc[:, col] = df_filtered.loc[:, col].astype(float)
                    except Exception as e:
                        df_filtered.loc[:, col] = df_filtered.loc[:, col].astype(str)
                        print(f'Error converting column {col} to float: {e}')



# Convert value column to float data type
convert_lst = ['RP', 'rp', 'RM', 'rm', 'CC', 'cc', 'tgt', 'ach', 'act', 'rate', 'payout',
               'ye_rate', 'amt', 'amount', 'deduct', 'rem1', 'rem2', 'rem3', 'rem4', 'total',
               'rm', 'ret', 'oth_clw', 'cf_clw']

for col in df_filtered.columns:
    for convert_item in convert_lst:
        if convert_item in col:
            try:
                # Check if the conversion to float is successful
                converted_values = pd.to_numeric(df_filtered.loc[:, col], errors='coerce')
                if not converted_values.isna().any():
                    df_filtered.loc[:, col] = converted_values.astype(float)
                else:
                    print(f'Warning: Unable to convert column {col} to float. Retaining original data type.')
            except Exception as e:
                print(f'Error converting column {col} to float: {e}. Retaining original data type.')
