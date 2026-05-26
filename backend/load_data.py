import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models import db, Movie
import pandas as pd

app = create_app()

with app.app_context():
    db.create_all()
    
    # Load movies from u.item
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
movies_df = pd.read_csv(os.path.join(BASE_DIR, 'data/u.item'), sep='|', encoding='latin-1',
                             header=None, usecols=range(24))
    
    genre_cols = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    genre_names = ['unknown','Action','Adventure','Animation','Childrens',
                   'Comedy','Crime','Documentary','Drama','Fantasy',
                   'Film-Noir','Horror','Musical','Mystery','Romance',
                   'Sci-Fi','Thriller','War','Western']
    
    count = 0
    for _, row in movies_df.iterrows():
        if Movie.query.get(int(row[0])):
            continue
        genres = [genre_names[i] for i, col in enumerate(genre_cols) if row[col] == 1]
        genre_str = '|'.join(genres) if genres else 'Unknown'
        
        movie = Movie(
            id=int(row[0]),
            title=str(row[1]),
            genres=genre_str,
            avg_rating=0.0,
            rating_count=0
        )
        db.session.add(movie)
        count += 1
    
    db.session.commit()
    print(f"Loaded {count} movies into database!")