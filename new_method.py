    def convert_columns_to_float(self, df):
        """
        Convert specified columns in the DataFrame to float data type.
        If not possible, retain the original data type. Convert None values to 0.

        Parameters:
        - df: DataFrame
        - convert_lst: List of substrings to identify columns for conversion

        Returns:
        - df: DataFrame after the column conversion
        """
        # Convert value column to float data type
        convert_lst = ['RP', 'rp', 'RM', 'rm', 'CC', 'cc', 'tgt', 'ach', 'act', 'rate', 'payout',
                       'ye_rate', 'amt', 'amount', 'deduct', 'rem1', 'rem2', 'rem3', 'rem4', 'total',
                       'rm', 'ret', 'oth_clw', 'cf_clw']
        df = df.copy().reset_index(drop=True)

        for col in df.columns:
            for convert_item in convert_lst:
                if convert_item in col:
                    try:
                        # Convert None values to 0
                        df[col] = df[col].fillna(0).astype(float)
                        
                        # Check if the conversion to float is successful
                        converted_values = pd.to_numeric(df.loc[:, col], errors='coerce')
                        
                        if not converted_values.isna().any():
                            df.loc[:, col] = converted_values.astype(float)
                        else:
                            print(f'Warning: Unable to convert column {col} to float. Retaining original data type.')
                            pass
                            
                    except Exception as e:
                        print(f'Error converting column {col} to float: {e}. Retaining original data type.')
                        return df
                        
        return df
         
    def process_data(self, df, insg_to_insx, sheet, cycle, month):
        header_row=int(insg_to_insx['insg_xls_start_row'])
        #print(insg_to_insx)

        # Transform data
        df.columns=df.iloc[header_row]
        df_cleaned=df.iloc[header_row+1:].reset_index(drop=True)
        #print(df_cleaned)
        
        # Process insx table
        df_cleaned=df_cleaned.loc[:, df_cleaned.columns.notna()]
        df_cleaned=df_cleaned.dropna(axis=1, how='all')  # Drop columns with all NaN values
        df_filtered=df_cleaned[df_cleaned.insx_staff_id.str.contains(r'^100[0-9]{5}$', regex=True, na=False)]             
        df_filtered.rename(columns=self.params_cols, inplace=True)
        #df_filtered.replace({np.nan: '', None: ''}, inplace=True)
        #df_filtered.where(pd.notnull(df), None)
        
        # Rename columns
        for col in self.params_cols:
            #print(col, params_cols[col])
            # Add new columns if not exist
            if self.params_cols[col] not in df_filtered.columns:
                df_filtered[self.params_cols[col]]=''

        df_filtered=self.convert_columns_to_float(df_filtered).copy()
        print(df_filtered.dtypes)
        print(df_filtered.shape)
                
        self.params_cols={
            'insx_cycle': cycle,
            'insx_month': month,
            'insx_version': insg_to_insx['insx_version'],
            'insx_row_count': df_filtered.shape[0],
            'insx_timestamp_upload': ''
        }
        
        # Update value in new added columns        
        df_filtered.loc[:, 'insx_month']=str(self.params_cols['insx_month'])
        df_filtered.loc[:, 'insx_cycle']=str(insg_to_insx['insg_cycle'])
        df_filtered.loc[:, 'insx_version']=str(self.params_cols['insx_version'])     
        df_filtered.loc[:, 'insx_src_file']=str(insg_to_insx['insg_src_file'])
 
        #if cycle == '1':
        #    df_filtered['insx_cycle']=self.params_cols['insx_cycle']
        #else:
        #    df_filtered['insx_cycle']=insg_to_insx['insg_cycle']
 

        #print(df_filtered.head())        
        #self.df=df_filtered
                   
        return df_filtered
