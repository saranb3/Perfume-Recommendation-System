import pandas as pd 

#load the dataset: 
try: 
    df = pd.read_csv('database/perfume_data.csv')
    print('Loaded dataset with UTF-8 encoding')
except: 
    df = pd.read_csv('database/perfume_data.csv', encoding='iso-8859-1')
    print('Loaded dataset with iso8859-1')

print(f"\n📊 Total rows: {len(df)}") #num of rowsm
print(f"📋 Columns: {df.columns.tolist()}")
print(f"\n🔍 First few rows:")
print(df.head())


