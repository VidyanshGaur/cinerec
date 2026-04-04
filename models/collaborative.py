import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def train_cf():
    df = pd.read_csv(os.path.join(DATA_DIR, 'u.data'),
                     sep='\t', names=['user_id','movie_id','score','timestamp'])
    df = df[['user_id','movie_id','score']]

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df, reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    model = SVD(n_epochs=20, lr_all=0.005, reg_all=0.02, random_state=42)
    model.fit(trainset)

    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    print(f"CF Model trained. RMSE: {rmse:.4f}")

    model_path = os.path.join(MODEL_DIR, 'cf_model.pkl')
    joblib.dump(model, model_path)
    print("CF model saved.")
    return model

def get_cf_recommendations(user_id, all_movie_ids, rated_movie_ids, top_n=20):
    model_path = os.path.join(MODEL_DIR, 'cf_model.pkl')
    model = joblib.load(model_path)

    unrated = [m for m in all_movie_ids if m not in rated_movie_ids]
    predictions = [(mid, model.predict(user_id, mid).est) for mid in unrated]
    predictions.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in predictions[:top_n]]

if __name__ == '__main__':
    train_cf()