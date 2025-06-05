import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle 

df = pd.read_csv('database/perfume_cleaned_database.csv')
print(f"Number of perfumes imported: {len(df)}") 

# See how notes are separated (comma + space)
print('Sample Notes: ')
for i in range(3): 
    print(f"{df['Notes'].iloc[i]}")

# After loading the CSV
print(f"\nChecking for null values:")
print(f"Null notes: {df['Notes'].isnull().sum()}")



# Check data types
print(f"Data type of Notes column: {df['Notes'].dtype}")

count_vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
note_vectors = count_vectorizer.fit_transform(df['Notes'])

# Explore what you created
print(f"Matrix shape: {note_vectors.shape}")
print(f"Total unique notes: {len(count_vectorizer.get_feature_names_out())}")

#Calculate cosine similarity between all perfumes 
print("\nCalculating similarities (this may take a moment)...")
similarity_matrix = cosine_similarity(note_vectors, dense_output=False)
print(f"Similarity matrix shape: {similarity_matrix.shape}")
print(similarity_matrix)