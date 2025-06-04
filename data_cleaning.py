import pandas as pd 
import numpy as np

#loaded the dataset with encoding='iso-8859-1'
df =  pd.read_csv('database/perfume_data.csv', encoding='iso-8859-1')
print(f"\n Total Rows: {len(df)}")

# Data Cleaning: finding rows that don't have notes

print(sum(df['Notes'].isnull())) 
missing_notes = df['Notes'].isnull() 
missing_notes_table = df[missing_notes]
print(missing_notes_table)




    


#Data cleaning: finding the rows without data
