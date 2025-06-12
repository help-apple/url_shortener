from flask import Flask
from models import db
from flask_login import LoginManager
from auth import auth
from dashboard import dashboard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorten.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)

# Tạo database (chạy 1 lần)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)