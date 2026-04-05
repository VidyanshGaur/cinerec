# 🎬 CineRec — Personalized Movie Recommendation Engine

A web-based movie recommendation system built with Python and Flask that uses Machine Learning to suggest personalized content to users.

> **SEPM Individual Project | The NorthCap University, Gurgaon**
> Roll No: 23CSU342 | Vidyansh Gaur | B.Tech CSE (AI/ML) — 6th Semester

## 🚀 Features
- User registration and login with bcrypt password hashing
- Browse and search 1682 movies
- Rate movies on a 1–5 star scale
- Content-Based Filtering — recommends similar movies based on genre
- Collaborative Filtering — SVD model trained on MovieLens 100K (RMSE: 0.9352)
- Hybrid Engine — 60% CF + 40% CBF weighted recommendations
- Cold start handling for new users

## 🛠️ Tech Stack
- Backend: Python 3.13, Flask
- Database: SQLite + SQLAlchemy
- ML: scikit-learn, scikit-surprise, pandas, numpy
- Frontend: HTML5, CSS3, Bootstrap 5
- Auth: Flask-Login, bcrypt
- Dataset: MovieLens 100K
- Testing: pytest

## ⚙️ Setup & Run

### 1. Clone the repo
git clone https://github.com/VidyanshGaur/recommendation-engine.git
cd recommendation-engine

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Load movies into database
cd backend
python load_data.py

### 5. Train ML models
cd ..
python models/train.py

### 6. Run the app
cd backend
python app.py

Open http://127.0.0.1:5000 in your browser.

## 🧪 Run Tests
pytest tests/ -v
Results: 10/10 tests passing

## 🤖 How Recommendations Work
User Ratings → Collaborative Filter (SVD) + Content-Based Filter (TF-IDF) → Hybrid Engine → Top 10 Recommendations

## 📊 Dataset Stats
- Total Ratings: 100,000
- Unique Users: 943
- Unique Movies: 1,682
- Sparsity: 93.7%

## 🔮 Future Enhancements
- Deep learning based recommendations
- Real-time model retraining
- Mobile responsive PWA
- Deployment on Render/Railway
