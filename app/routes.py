from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddAuthor, AddGenre, AddProvider, AddBook, Delete
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Provider, Genre, Author, Book, BookAuthor, BookGenre
from werkzeug.urls import url_parse

def login_required(role = False):
    def wrapper(fn):
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return app.login_manager.unauthorized()
            urole = current_user.isEmployee
            if ((role != False) and (urole != True)):
                return app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/special', methods=['GET', 'POST'])
@login_required(role=True)
def index():
    genres= [(c.id, c.name) for c in Genre.query.all()]
    authors= [(c.id, (c.name+' '+c.surname)) for c in Author.query.all()]
    GenreForm = AddGenre(prefix="GenreForm")
    AuthorForm = AddAuthor(prefix="AuthorForm")
    ProviderForm = AddProvider(prefix="ProviderForm")
    BookForm = AddBook(prefix="BookForm")
    DeleteForm = Delete(prefix="Delete")

    BookForm.genres.choices = genres
    BookForm.authors.choices = authors

    if BookForm.submit1.data and BookForm.validate():
        book = Book(name=BookForm.name.data, price=BookForm.price.data,
        year=BookForm.year.data)
        for i in BookForm.genres.data:
            genre = Genre.query.filter_by(id=i).first()
            book.genres.append(genre)
        for k in BookForm.authors.data:
            author = Author.query.filter_by(id=k).first()
            book.authors.append(author)
        db.session.add(book)
        db.session.commit()
        BookForm.name.data=''
        BookForm.price.data=''
        BookForm.year.data=''
        BookForm.authors.data=[]
        BookForm.genres.data=[]
    if GenreForm.submit2.data and GenreForm.validate():
        genre = Genre(name=GenreForm.name.data)
        db.session.add(genre)
        db.session.commit()
        genres= [(c.id, c.name) for c in Genre.query.all()]
        GenreForm.name.data=''
    if AuthorForm.submit3.data and AuthorForm.validate():
        author = Author(name=AuthorForm.name.data, surname=AuthorForm.surname.data,)
        db.session.add(author)
        db.session.commit()
        authors= [(c.id, (c.name+' '+c.surname)) for c in Author.query.all()]
        AuthorForm.name.data=''
        AuthorForm.surname.data=''
    if ProviderForm.submit4.data and ProviderForm.validate():
        provider = Provider(name=ProviderForm.name.data,
        address=ProviderForm.address.data, phone=ProviderForm.phone.data,)
        db.session.add(provider)
        db.session.commit()
        ProviderForm.name.data=''
        ProviderForm.phone.data=''
        ProviderForm.address.data=''
    if DeleteForm.submit5.data and DeleteForm.validate():
        if DeleteForm.table.data == 1: a = Book.query.filter_by(id=DeleteForm.id.data).first()
        elif DeleteForm.table.data == 2: a = Genre.query.filter_by(id=DeleteForm.id.data).first()
        elif DeleteForm.table.data == 3: a = Author.query.filter_by(id=DeleteForm.id.data).first()
        else: a = Provider.query.filter_by(id=DeleteForm.id.data).first()
        if a is not None:
            db.session.delete(a)
            db.session.commit()
        DeleteForm.id.data=''
        DeleteForm.table.data=[]
    return render_template("special.html", title='Home Page', GenreForm=GenreForm,
    AuthorForm = AuthorForm, ProviderForm = ProviderForm, BookForm = BookForm, DeleteForm = DeleteForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(phone=form.phone.data,
        name=form.name.data, surname=form.surname.data, address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)

@app.route('/regforemployee', methods=['GET', 'POST'])
def registerforemployee():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(phone=form.phone.data,
        name=form.name.data, surname=form.surname.data, address=form.address.data, isEmployee=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('regforemployee.html', title='Register', form=form)
