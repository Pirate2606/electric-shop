from models import app, db, User, MyCart
from flask import render_template, url_for, request, redirect, request, g
from wtforms import ValidationError
from flask_login import login_user, login_required, logout_user, current_user
from forms import RegisterUser, LoginUser
from flask_migrate import Migrate
from sendMail import send_mail
from flask_uploads import UploadSet, configure_uploads, IMAGES


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/profiles'

Migrate(app, db)
configure_uploads(app, photos)

val = list()
cart = list()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
@login_required
def products():
    return render_template('products.html')


@app.route('/mycart', methods = ['GET', 'POST'])
@login_required
def myCart():

    g.user = current_user.get_id()
    id = int(g.user)
    if request.args.get('val') is not None:
        val.append(request.args.get('val'))
        item = MyCart(val[-1], id)
        db.session.add(item)
        db.session.commit()

    item = MyCart.query.filter_by(user_id = id)
    cart = item.all()

    return render_template('mycart.html', cart = cart)


@app.route('/<product>', methods = ['GET', 'POST'])
@login_required
def individualProduct(product):
    return render_template('individual_product.html', product = product)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods = ['POST', 'GET'])
def login():

    form = LoginUser()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if user is None:
            return render_template('not_registered.html')

        elif user.check_password(form.password.data) == False:
            return render_template('login.html', form = form, flag = True)

        elif user.check_password(form.password.data):
            login_user(user, remember = form.check.data)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)

    return render_template('login.html', form = form, flag = False)


@app.route('/register', methods = ['POST', 'GET'])
def register():

    form = RegisterUser()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        username = form.username.data

        try:
            form.check_mail(email)
        except ValidationError as error:
            return render_template('already_exist.html', error = repr(error))

        try:
            form.check_username(username)
        except ValidationError as error:
            return render_template('already_exist.html', error = repr(error))

        user = User(email, username, password, 'default.png')
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email = form.email.data).first()
        mail = user.email
        send_mail(mail)

        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    g.user = current_user.get_id()
    id = int(g.user)
    user = User.query.filter_by(id = id).first()
    email = user.email
    username = user.username
    image_filename = user.profile_image

    if request.method == 'POST' and 'thefile' in request.files:
        try:
            image_filename = photos.save(request.files['thefile'])
        except:
            pass
        user.profile_image = image_filename
        db.session.add(user)
        db.session.commit()

    return render_template('profile.html', email = email, username = username, file_name = image_filename)



if __name__ == '__main__':
    app.run(debug = True)
