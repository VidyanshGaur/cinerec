import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

GENRE_COLS = list(range(6, 24))
GENRE_NAMES = ['unknown','Action','Adventure','Animation','Childrens',
               'Comedy','Crime','Documentary','Drama','Fantasy',
               'Film-Noir','Horror','Musical','Mystery','Romance',
               'Sci-Fi','Thriller','War','Western']

def load_movies_from_csv():
    movies_df = pd.read_csv(os.path.join(DATA_DIR, 'u.item'),
                             sep='|', encoding='latin-1', header=None,
                             usecols=range(24))
    rows = []
    for _, row in movies_df.iterrows():
        genres = [GENRE_NAMES[i] for i, col in enumerate(GENRE_COLS) if row[col] == 1]
        rows.append({'id': int(row[0]), 'title': str(row[1]), 'genres': '|'.join(genres) if genres else 'Unknown'})
    return pd.DataFrame(rows)

def train_cbf():
    df = load_movies_from_csv()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['genres'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    model_path = os.path.join(MODEL_DIR, 'cbf_model.pkl')
    joblib.dump((cosine_sim, df), model_path)
    print(f"CBF model saved. Matrix shape: {cosine_sim.shape}")
    return cosine_sim, df

def get_similar_movies(movie_id, top_n=10):
    model_path = os.path.join(MODEL_DIR, 'cbf_model.pkl')
    cosine_sim, df = joblib.load(model_path)

    idx_list = df[df['id'] == movie_id].index.tolist()
    if not idx_list:
        return []

    idx = idx_list[0]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    return [int(df.iloc[i[0]]['id']) for i in scores]

if __name__ == '__main__':
    train_cbf()