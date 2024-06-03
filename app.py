from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from extensions import db
from flask_migrate import Migrate
from forms import BookForm, MemberForm
from models import Book, Member
from main import main  # Import blueprint

from db import MysqlDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)


# inisisalisasi mysql
MysqlDB.init_app(app)


# Inisialisasi Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprint
app.register_blueprint(main, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Contoh penggunaan generate_password_hash untuk menghasilkan hash password
    hashed_password = generate_password_hash('adminpassword', method='pbkdf2:sha512')
    print(hashed_password)  # Cetak hash password untuk memeriksa

    app.run(debug=True)
