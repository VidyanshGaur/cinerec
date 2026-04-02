from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Movie, Rating
import joblib
import os

recommend_bp = Blueprint('recommend', __name__)

def get_popular_movies(n=10):
    movies = Movie.query.order_by(Movie.avg_rating.desc(), Movie.rating_count.desc()).limit(n).all()
    return [{'id': m.id, 'title': m.title, 'genres': m.genres, 'avg_rating': round(m.avg_rating, 2)} for m in movies]

@recommend_bp.route('/recommend')
@login_required
def recommend():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    
    # Cold start — less than 5 ratings
    if len(user_ratings) < 5:
        movies = get_popular_movies(10)
        return render_template('recommend.html', 
                               movies=movies, 
                               message="Rate more movies to get personalized recommendations!",
                               is_cold_start=True)
    
    # Check if model exists
    model_path = os.path.join(os.path.dirname(__file__), '../../models/hybrid_model.pkl')
    
    if not os.path.exists(model_path):
        movies = get_popular_movies(10)
        return render_template('recommend.html', 
                               movies=movies,
                               message="Model training in progress. Showing top rated movies.",
                               is_cold_start=True)
    
    try:
        hybrid_model = joblib.load(model_path)
        rated_movie_ids = [r.movie_id for r in user_ratings]
        all_movie_ids = [m.id for m in Movie.query.all()]
        
        recommended_ids = hybrid_model.recommend(
            user_id=current_user.id,
            all_movie_ids=all_movie_ids,
            rated_movie_ids=rated_movie_ids,
            top_n=10
        )
        
        movies = []
        for mid in recommended_ids:
            m = Movie.query.get(mid)
            if m:
                movies.append({
                    'id': m.id, 
                    'title': m.title, 
                    'genres': m.genres, 
                    'avg_rating': round(m.avg_rating, 2)
                })
        
        return render_template('recommend.html', movies=movies, is_cold_start=False)
    
    except Exception as e:
        movies = get_popular_movies(10)
        return render_template('recommend.html', 
                               movies=movies,
                               message="Showing top rated movies.",
                               is_cold_start=True)

@recommend_bp.route('/api/recommend')
@login_required
def api_recommend():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    
    if len(user_ratings) < 5:
        return jsonify({
            'recommendations': get_popular_movies(10),
            'type': 'popular',
            'message': 'Rate more movies for personalized recommendations'
        })
    
    return jsonify({
        'recommendations': get_popular_movies(10),
        'type': 'popular'
    })