from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    cover_image = StringField('Cover Image URL')  # Field baru
    submit = SubmitField('Add Book')

class MemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Member')

class AddShoeForm(FlaskForm):
    colors = [('Hitam', 'Hitam'), ('Putih', 'Putih'), ('Abu', 'Abu'), ('Coklat', 'Coklat'), ('Merah', 'Merah')]
    types = [('Sepatu_Pria', 'Sepatu Pria'), ('Sepatu_Wanita', 'Sepatu Wanita'), ('Sepatu_Anak', 'Sepatu Anak')]

    # merk sepatu
    shoe_brand = StringField('Shoe Brand', validators=[DataRequired()])
    # warna sepatu
    # drop down 'Hitam', 'Putih', 'Abu', 'Coklat', 'Merah
    shoe_color = SelectField('Shoe Color', choices=colors, validators=[DataRequired()])
    # jenis sepatu
    # drop down 'Sepatu_Pria', 'Sepatu_Wanita', 'Sepatu_Anak
    shoe_type = SelectField('Shoe Type', choices=types, validators=[DataRequired()])
    # bahan sepatu
    shoe_material = StringField('Shoe Material', validators=[DataRequired()])
    # deskripsi sepatu
    shoe_description = StringField('Shoe Description', validators=[])
    # tanggal rilis
    release_date = DateTimeLocalField('Release Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])


