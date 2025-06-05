import pandas as pd 
import numpy as np
from pathlib import Path

#loaded the dataset with encoding='iso-8859-1'
df =  pd.read_csv('database/perfume_data.csv', encoding='iso-8859-1')
print(f"\n Total Rows: {len(df)}")

# Data Cleaning: finding rows that don't have notes

print(sum(df['Notes'].isnull())) 
missing_notes = df['Notes'].isnull() 
missing_notes_table = df[missing_notes]
print(missing_notes_table)

# Modify the dataset to only include perfumes with notes  for cosine similarity
perfume_cleaned_dataset = df.dropna(subset=['Notes']) 

# Clean the notes column for excess space and capitalization consistency
perfume_cleaned_dataset['Notes'] = perfume_cleaned_dataset['Notes'].str.strip().str.lower() 


# Check how many rows remain
print(f"\nAfter removing missing notes: {len(perfume_cleaned_dataset)} perfumes")
print(f"Removed: {len(df) - len(perfume_cleaned_dataset)} perfumes")

# Check if cleaning worked
print("\nSample of cleaned notes:")
for i in range(3):
    print(f"'{perfume_cleaned_dataset['Notes'].iloc[i]}'")
    

# Save it
filepath = Path('database/perfume_cleaned_database.csv')
perfume_cleaned_dataset.to_csv(filepath, index=False)



