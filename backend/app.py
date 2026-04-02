from flask import Flask
from flask_login import LoginManager
from models import db, User
import os

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    app.config['SECRET_KEY'] = 'sepm-rec-engine-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rec_engine.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.movies import movies_bp
    from routes.recommend import recommend_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(recommend_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database created!")
    app.run(debug=True)