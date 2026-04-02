from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Movie, Rating

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
@movies_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's rated movie ids
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    rated_ids = [r.movie_id for r in user_ratings]
    
    # Top rated movies for display
    top_movies = Movie.query.order_by(Movie.avg_rating.desc()).limit(20).all()
    
    return render_template('dashboard.html', 
                           movies=top_movies, 
                           rated_ids=rated_ids,
                           user=current_user)

@movies_bp.route('/browse')
@login_required
def browse():
    search = request.args.get('search', '')
    if search:
        movies = Movie.query.filter(Movie.title.ilike(f'%{search}%')).all()
    else:
        movies = Movie.query.order_by(Movie.rating_count.desc()).all()
    
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    rated_ids = [r.movie_id for r in user_ratings]
    
    return render_template('browse.html', movies=movies, rated_ids=rated_ids, search=search)

@movies_bp.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    user_rating = Rating.query.filter_by(
        user_id=current_user.id, 
        movie_id=movie_id
    ).first()
    
    return render_template('movie.html', movie=movie, user_rating=user_rating)

@movies_bp.route('/rate', methods=['POST'])
@login_required
def rate_movie():
    movie_id = request.form.get('movie_id', type=int)
    score = request.form.get('score', type=float)
    
    if not movie_id or not score or score < 1 or score > 5:
        return jsonify({'error': 'Invalid rating'}), 400
    
    # Check if already rated
    existing = Rating.query.filter_by(
        user_id=current_user.id, 
        movie_id=movie_id
    ).first()
    
    if existing:
        existing.score = score
    else:
        new_rating = Rating(user_id=current_user.id, movie_id=movie_id, score=score)
        db.session.add(new_rating)
    
    # Update movie avg rating
    movie = Movie.query.get(movie_id)
    all_ratings = Rating.query.filter_by(movie_id=movie_id).all()
    movie.avg_rating = sum(r.score for r in all_ratings) / len(all_ratings)
    movie.rating_count = len(all_ratings)
    
    db.session.commit()
    return jsonify({'success': True, 'avg_rating': round(movie.avg_rating, 2)})