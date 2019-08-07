from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, session
from app import app
from functools import wraps
from app.forms import LoginForm, RegistrationForm, AddAuthor, AddGenre, AddProvider, AddBook, Delete, AddProvPrice, BookSearch, MakePOrder
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Provider, Genre, Author, Book, BookAuthor, Warehouse, OrderToProvider
from app.models import BookGenre, OrderFromCustomer, OrderCbooks, CustomerBill, ProvPrices, OrderPbooks
from werkzeug.urls import url_parse

def sess():
    if 'cart' in session:
        return len(session['cart'])
    else:
        return 0

def mysort(x):
    return x[0].id
def mysortP(x):
    return int(a[1])
def login_required(role = False):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return app.login_manager.unauthorized()
            urole = current_user.isEmployee
            if ((role != False) and (urole != True)):
                return app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    Search = BookSearch(prefix="Search")
    books = Book.query.all()
    genres= [(c.id, c.name) for c in Genre.query.all()]
    authors= [(c.id, (c.name+' '+c.surname)) for c in Author.query.all()]
    Search.genres.choices = genres
    Search.authors.choices = authors
    if Search.submit.data and Search.validate():
        gen = Search.genres.data
        aut = Search.authors.data
        if gen == [] and aut == []:
            books = Book.query.all()
        elif gen != [] and aut == []:
            books = Book.query.filter(Book.genres.any(Genre.id.in_(gen))).all()
        elif gen == [] and aut != []:
            books = Book.query.filter(Book.authors.any(Author.id.in_(aut))).all()
        else: books = Book.query.filter((Book.genres.any(Genre.id.in_(gen))), (Book.authors.any(Author.id.in_(aut)))).all()
    length = len(books)
    return render_template("index.html", title='Home Page', books=books, length=length, ses=sess(), Search=Search)

@app.route('/addporder/<int:Pid>', methods=['GET', 'POST'])
@login_required(role=True)
def addporder(Pid):
    prices = ProvPrices.query.filter_by(ProviderId=Pid).all()
    bookInfo = []
    listBooks = []
    for price in prices:
        bookInfo = []
        book = Book.query.filter_by(id = price.BookId).first()
        bookInfo = [book.name, price.Price, book.id]
        listBooks.append(bookInfo)
    books = []
    if 'pcart'+str(Pid) in session:
        for i in session['pcart'+str(Pid)]:
            book = Book.query.filter_by(id=i).first()
            books.append(book)
        booksnew = []
        for i in set(books):
            price = ProvPrices.query.filter_by(ProviderId=Pid, BookId = i.id).first()
            booksnew.append([i.id, i.name, price.Price,books.count(i)])
        booksnew.sort()
        lengthCart = len(booksnew)
    else:
        session.modified = True
        session['pcart'+str(Pid)] = []
        booksnew = []
        lengthCart = len(booksnew)

    return render_template("addporder.html", ses=sess(), Books=listBooks,
     length=len(listBooks), Pid=Pid, lengthCart=lengthCart, booksCart=booksnew, )


@app.route('/special', methods=['GET', 'POST'])
@login_required(role=True)
def special():
    genres= [(c.id, c.name) for c in Genre.query.all()]
    authors= [(c.id, (c.name+' '+c.surname)) for c in Author.query.all()]
    providers= [(c.id, c.name) for c in Provider.query.all()]
    books= [(c.id, c.name) for c in Book.query.all()]
    GenreForm = AddGenre(prefix="GenreForm")
    AddPrice = AddProvPrice(prefix='AddPrice')
    AuthorForm = AddAuthor(prefix="AuthorForm")
    ProviderForm = AddProvider(prefix="ProviderForm")
    BookForm = AddBook(prefix="BookForm")
    DeleteForm = Delete(prefix="Delete")
    MakeOrder = MakePOrder(prefix='MakeOrder')

    MakeOrder.provider.choices = providers
    BookForm.genres.choices = genres
    BookForm.authors.choices = authors
    AddPrice.provider.choices = providers
    AddPrice.book.choices = books

    if BookForm.submit1.data and BookForm.validate():
        book = Book(name=BookForm.name.data, price=BookForm.price.data,
        year=BookForm.year.data)
        wrh = Warehouse(numberOfBooks=0)
        book.warehouse = wrh
        for i in BookForm.genres.data:
            genre = Genre.query.filter_by(id=i).first()
            book.genres.append(genre)
        for k in BookForm.authors.data:
            author = Author.query.filter_by(id=k).first()
            book.authors.append(author)
        db.session.add(book)
        db.session.commit()
        books= [(c.id, c.name) for c in Book.query.all()]
        AddPrice.book.choices = books
        BookForm.name.data=''
        BookForm.price.data=''
        BookForm.year.data=''
        BookForm.authors.data=[]
        BookForm.genres.data=[]
    if AddPrice.submit6.data and AddPrice.validate():
        price = ProvPrices.query.filter_by(ProviderId=AddPrice.provider.data, BookId=AddPrice.book.data).first()
        if price is None:
            pPrice = ProvPrices(Price=AddPrice.price.data, ProviderId=AddPrice.provider.data,
            BookId=AddPrice.book.data)
            db.session.add(pPrice)
            db.session.commit()
        else:
            price.Price = AddPrice.price.data
            db.session.commit()
        AddPrice.price.data=''
        AddPrice.provider.data=[]
        AddPrice.book.data=[]
    if MakeOrder.submit7.data and MakeOrder.validate():
        return redirect(url_for('addporder', Pid=MakeOrder.provider.data))
    if GenreForm.submit2.data and GenreForm.validate():
        genre = Genre(name=GenreForm.name.data)
        db.session.add(genre)
        db.session.commit()
        genres= [(c.id, c.name) for c in Genre.query.all()]
        BookForm.genres.choices = genres
        GenreForm.name.data=''
    if AuthorForm.submit3.data and AuthorForm.validate():
        author = Author(name=AuthorForm.name.data, surname=AuthorForm.surname.data,)
        db.session.add(author)
        db.session.commit()
        authors= [(c.id, (c.name+' '+c.surname)) for c in Author.query.all()]
        BookForm.authors.choices = authors
        AuthorForm.name.data=''
        AuthorForm.surname.data=''
    if ProviderForm.submit4.data and ProviderForm.validate():
        provider = Provider(name=ProviderForm.name.data,
        address=ProviderForm.address.data, phone=ProviderForm.phone.data,)
        db.session.add(provider)
        db.session.commit()
        providers= [(c.id, c.name) for c in Provider.query.all()]
        AddPrice.provider.choices = providers
        ProviderForm.name.data=''
        ProviderForm.phone.data=''
        ProviderForm.address.data=''
    if DeleteForm.submit5.data and DeleteForm.validate():
        if DeleteForm.table.data == 1:
            wrh = Warehouse.query.filter_by(BookId=DeleteForm.id.data).first()
            a = Book.query.filter_by(id=DeleteForm.id.data).first()
        elif DeleteForm.table.data == 2: a = Genre.query.filter_by(id=DeleteForm.id.data).first()
        elif DeleteForm.table.data == 3: a = Author.query.filter_by(id=DeleteForm.id.data).first()
        else: a = Provider.query.filter_by(id=DeleteForm.id.data).first()
        if a is not None:
            db.session.delete(a)
            db.session.commit()
        if wrh is not None:
            db.session.delete(wrh)
            db.session.commit()
        DeleteForm.id.data=''
        DeleteForm.table.data=[]
    return render_template("special.html", title='Home Page', GenreForm=GenreForm,
    AuthorForm = AuthorForm, ProviderForm = ProviderForm, BookForm = BookForm,
    DeleteForm = DeleteForm,AddPrice=AddPrice, MakeOrder=MakeOrder, ses=sess())

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
    return render_template("login.html", title='Sign in', form=form, ses=sess())

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
    return render_template('reg.html', title='Register', form=form, ses=sess())

@app.route('/add', methods=['POST', 'GET'])
def add():
    book = Book.query.filter_by(id=request.form["buy"]).first_or_404()
    if 'cart' in session:
        session.modified = True
        session['cart'].append(book.id)
    else:
        session.modified = True
        session['cart'] = []
    return redirect(url_for('index'))

@app.route('/addProv', methods=['POST', 'GET'])
@login_required(role=True)
def addProv():
    book = Book.query.filter_by(id=request.form["buyP"]).first()
    Pid = request.form["Pid"]
    if 'pcart'+str(Pid) in session:
        session.modified = True
        session['pcart'+str(Pid)].append(book.id)
    else:
        session.modified = True
        session['pcart'+str(Pid)] = []
    return redirect(url_for('addporder', Pid=Pid))



@app.route('/delete', methods=['POST', 'GET'])
def delete():
    book = Book.query.filter_by(id=request.form["del"]).first_or_404()
    session.modified = True
    timeses = session['cart']
    timeses.remove(int(book.id))
    session['cart'] = timeses
    return redirect(url_for('cart'))

@app.route('/deleteP', methods=['POST', 'GET'])
@login_required(role=True)
def deleteP():
    book = Book.query.filter_by(id=request.form["delP"]).first_or_404()
    Pid = request.form["Pid"]
    session.modified = True
    timeses = session['pcart'+str(Pid)]
    timeses.remove(int(book.id))
    session['pcart'+str(Pid)] = timeses
    return redirect(url_for('addporder', Pid=Pid))

@app.route('/orderscheck', methods=['POST', 'GET'])
@login_required(role=True)
def orderscheck():
    
    return render_template('orders.html', ses=sess())

@app.route('/orderprov', methods=['POST', 'GET'])
@login_required(role=True)
def make_order_P():
    Pid = request.form["Pid"]
    session.modified = True
    if current_user.is_authenticated:
        order = OrderToProvider(EmployeeId=current_user.id, ProviderId=Pid)
        db.session.add(order)
        db.session.commit()
        books =[]
        if 'pcart'+str(Pid) in session:
            for i in session['pcart'+str(Pid)]:
                bookWarehouse = Warehouse.query.filter_by(id=i).first()
                bookWarehouse.numberOfBooks +=1
                book = Book.query.filter_by(id=i).first()
                books.append(book)
            booksnew = []
            for i in set(books):
                booksnew.append([i,books.count(i)])
            booksnew.sort(key=mysort)
            for i in booksnew:
                stat = OrderPbooks(OrderPId=order.id,
                BookId=i[0].id, numberOfBooks=i[1])
                db.session.add(stat)
                db.session.commit()

            for i in reversed(range(0,len(session['pcart'+str(Pid)]))):
                session['pcart'+str(Pid)].pop(i)
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/thanks', methods=['POST', 'GET'])
def thanks():
    return render_template('thanks.html', title='Thanks!', ses=sess())

@app.route('/deleteall', methods=['POST', 'GET'])
def delete_all():
    session.modified = True
    for i in reversed(range(0,len(session['cart']))):
        session['cart'].pop(i)
    return redirect(url_for('cart'))

@app.route('/deleteallprov', methods=['POST', 'GET'])
def delete_all_P():
    Pid = request.form["Pid"]
    session.modified = True
    for i in reversed(range(0,len(session['pcart'+str(Pid)]))):
        session['pcart'+str(Pid)].pop(i)
    return redirect(url_for('addporder', Pid=Pid))

@app.route('/order', methods=['POST', 'GET'])
def make_order():
    session.modified = True
    if current_user.is_authenticated:
        order = OrderFromCustomer(CustomerId=current_user.id)
        db.session.add(order)
        db.session.commit()
        books =[]
        if 'cart' in session:
            for i in session['cart']:
                book = Book.query.filter_by(id=i).first()
                books.append(book)
            booksnew = []
            for i in set(books):
                booksnew.append([i,books.count(i)])
            booksnew.sort(key=mysort)
            for i in booksnew:
                stat = OrderCbooks(OrderCId=order.id,
                BookId=i[0].id, numberOfBooks=i[1])
                db.session.add(stat)
                db.session.commit()
            for i in reversed(range(0,len(session['cart']))):
                session['cart'].pop(i)
        return redirect(url_for('thanks'))
    else:
        return redirect(url_for('login'))

@app.route('/cart', methods=['POST', 'GET'])
def cart():
    books = []
    if 'cart' in session:
        for i in session['cart']:
            book = Book.query.filter_by(id=i).first()
            books.append(book)
        booksnew = []
        for i in set(books):
            booksnew.append([i,books.count(i)])
        booksnew.sort(key=mysort)
        length = len(booksnew)
    else:
        session.modified = True
        session['cart'] = []
        booksnew = []
        length = len(booksnew)
    return render_template('cart.html', title='Cart', books=booksnew, length=length, ses=sess())


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if current_user.is_authenticated:
        orders = OrderFromCustomer.query.filter_by(CustomerId=current_user.id).order_by(OrderFromCustomer.id.desc()).all()
        bills = []
        numberOfBooks = []
        for i in orders:
            if i.bill is not None:
                bills.append(i.bill)
        billen = len(list(bills))
        orderlen = len(list(orders))
        return render_template('profile.html', title='Cart', ses=sess(), user=current_user,
        orders=orders, bills=bills, billen=billen, orderlen=orderlen, num=numberOfBooks)
    else:
        return redirect(url_for('login'))


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
    return render_template('regforemployee.html', title='Register', form=form, ses=sess())
