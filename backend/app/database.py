# backend/app/database.py
import sqlite3
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

DATABASE_PATH = "perfumes.db"
SIMILARITY_MATRIX_PATH = "similarity_matrix.pkl"

def init_db():
    """Initialize database and precompute similarity matrix"""
    # Load your cleaned CSV - correct path for your directory structure
    df = pd.read_csv('database/perfume_cleaned_database.csv')
    print(f"Loaded {len(df)} perfumes from CSV")
    
    # Create SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    df.to_sql('perfumes', conn, if_exists='replace', index=False)
    conn.close()
    print("Database created successfully")
    
    # Precompute similarity matrix
    compute_similarity_matrix(df)
    print("Database and similarity matrix initialized!")

def notes_tokenizer(text):
    """Tokenizer function for notes (can be pickled)"""
    return text.split(', ')

def compute_similarity_matrix(df):
    """Compute and save similarity matrix"""
    print("Computing similarity matrix...")
    count_vectorizer = CountVectorizer(tokenizer=notes_tokenizer)
    note_vectors = count_vectorizer.fit_transform(df['Notes'])
    similarity_matrix = cosine_similarity(note_vectors, dense_output=False)
    
    # Save similarity matrix and feature names (not the vectorizer with lambda)
    with open(SIMILARITY_MATRIX_PATH, 'wb') as f:
        pickle.dump({
            'similarity_matrix': similarity_matrix,
            'feature_names': count_vectorizer.get_feature_names_out()
        }, f)
    print(f"Similarity matrix saved with shape: {similarity_matrix.shape}")

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_PATH)

def load_similarity_data():
    """Load precomputed similarity data"""
    with open(SIMILARITY_MATRIX_PATH, 'rb') as f:
        return pickle.load(f)