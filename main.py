from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.utils import secure_filename
import os
from extensions import db
from forms import BookForm, MemberForm, LoginForm, AddShoeForm
from models import Book, Member
from flask_login import login_required, logout_user
from flask import request, redirect, url_for, flash
from flask import render_template, redirect, url_for, flash
from forms import BookForm
from db import MysqlDB

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def valid_login(email, password):
    return email == 'tribhuana@example.com' and password == 'admin123'

def titleGuard(title):
    return len(title) <= 32

def middleware():
    if 'auth' not in session:
        session['auth'] = 'false'
    if session['auth'] != 'true':
        return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if valid_login(email, password):
            flash('Login successful!', 'success')
            session['auth'] = 'true'
            return redirect(url_for('main.index'))
        else:
            session['auth'] = 'false'
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/account')
def account():
    return render_template('account.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))

@app.before_request
def check_auth():
    if not session.get('auth') == 'true' and request.endpoint != 'main.login':
        return redirect(url_for('main.login'))

@app.before_request
def check_auth():
    if not session.get('auth') == 'true' and request.endpoint != 'main.login':
        return redirect(url_for('main.login'))

@app.route('/home')
def home():
    user_login_name = request.args.get('username')
    return render_template('home.html', user_login_name=user_login_name)

@main.route('/books', methods=['GET'])
def show_books():
    if middleware() is not None:
        return middleware()

    books = Book.query.all()
    return render_template('books.html', books=books)

@main.route('/', methods=['GET'])
def index():
    if middleware() is not None:
        return middleware()

    search_query = request.args.get('search')
    if search_query:
        books = Book.query.filter((Book.title.contains(search_query)) | (Book.isbn.contains(search_query))).all()
        books = sorted(books, key=lambda x: (search_query.lower() in x.title.lower(), search_query.lower() in x.isbn.lower()), reverse=True)
    else:
        books = Book.query.all()
    return render_template('index.html', books=books, search_query=search_query)

@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if middleware() is not None:
        return middleware()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        year = request.form['year']
        publisher = request.form['publisher']
        cover_image = request.files['cover_image']

        if not titleGuard(title):
            flash('Title cannot exceed 32 characters!', 'error')
            return redirect(url_for('main.add_book'))

        if cover_image and allowed_file(cover_image.filename):
            filename = secure_filename(cover_image.filename)
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_book = Book(title=title, author=author, isbn=isbn, year=year, publisher=publisher, cover_image=filename)
            db.session.add(new_book)
            db.session.commit()

            flash('Book added successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid image file format!', 'error')
            return redirect(url_for('main.add_book'))

    return render_template('add_book.html')

@main.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if middleware() is not None:
        return middleware()

    form = MemberForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        
        new_member = Member(name=name, email=email)
        db.session.add(new_member)
        db.session.commit()

        flash('Member added successfully!', 'success')
        return redirect(url_for('main.index'))

    members = Member.query.all()
    return render_template('add_member.html', form=form, members=members)

@main.route('/show_profile')
def show_profile():
    if 'auth' not in session or session['auth'] != 'true':
        flash('You are not logged in!', 'danger')
        return redirect(url_for('main.login'))
    # You can fetch user profile information here from your database or session
    user_profile = {'name': 'John Doe', 'email': 'johndoe@example.com'}
    return render_template('profile.html', user_profile=user_profile)

@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if middleware() is not None:
        return middleware()

    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)  # Create an instance of BookForm with the book object
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(book)  # Update the book object with form data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_book.html', form=form, book=book)  # Pass form to the template

@main.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    if middleware() is not None:
        return middleware()

    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('delete_book.html', book=book)

@main.route('/members', methods=['GET'])
def show_members():
    if middleware() is not None:
        return middleware()

    members = Member.query.all()
    return render_template('members.html', members=members)

@main.route('/add_shoe', methods=['GET', 'POST'])
def add_shoe():
    if middleware() is not None:
        return middleware()

    form = AddShoeForm()
    print(form.errors)
    if request.method == 'POST' and form.validate_on_submit():
        print('Form validated')
        shoe_brand = form.shoe_brand.data
        shoe_color = form.shoe_color.data
        shoe_type = form.shoe_type.data
        shoe_material = form.shoe_material.data
        shoe_description = form.shoe_description.data
        release_date = form.release_date.data

        # tambah ke mysql
        cursor = MysqlDB.get_cursor()
        if cursor is None:
            flash('Database not initialized', 'error')
            return redirect(url_for('main.add_shoe'))
        try :
            cursor.execute('INSERT INTO form_master_sepatu (shoe_brand, shoe_color, shoe_type, shoe_material, shoe_description, release_date) VALUES (%s, %s, %s, %s, %s, %s)', (shoe_brand, shoe_color, shoe_type, shoe_material, shoe_description, release_date))
            MysqlDB.commit()
            flash('Shoe added successfully!', 'success')
        except Exception as e:
            flash('Failed to add shoe!', 'error')
            print(e)
            MysqlDB.close()
            return redirect(url_for('main.add_shoe'))
        return redirect(url_for('main.index'))

    return render_template('add_shoe.html', form=form)
