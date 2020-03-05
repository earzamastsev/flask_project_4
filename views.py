from flask import session, request, render_template, abort, flash, redirect
from models import MealModel, CategoryModel, UserModel, OrderModel
from sqlalchemy.sql.expression import func
from app import app, db
from forms import RegisterForm, OrderForm, LoginForm


@app.route('/')
def index():
    categories = db.session.query(CategoryModel).all()
    cat_meals_dict = {}
    for category in categories:
        meals = db.session.query(MealModel).filter(MealModel.category == category) \
            .order_by(func.random()) \
            .limit(3) \
            .all()
        cat_meals_dict[category] = meals
    return render_template('main.html', meals=cat_meals_dict, session=session)


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    if form.validate_on_submit():
        order = OrderModel()
        user = session['user_id']
        if not user:
            user = UserModel(name=form.name.data, \
                             email=form.email.data, \
                             address=form.address.data, \
                             phone=form.phone.data)
            db.session.add(user)
            db.session.commit()

        else:
            user = db.session.query(UserModel).get(session['user_id'])

        order.users = user
        order.summa = sum(list(map(int, session['cart_price'])))
        meals = list(map(int, session['cart_id']))
        for meal in meals:
            meal = db.session.query(MealModel).get(meal)
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()
        session['cart_id'] = []
        session['cart_price'] = []
        return redirect('/ordered/')

    if session['user_id']:
        user = db.session.query(UserModel).get(session['user_id'])
        form.name.data = user.name
        form.email.data = user.email
        form.address.data = user.address
        form.phone.data = user.phone
    meals = []
    for meal in session['cart_id']:
        meal = db.session.query(MealModel).get(meal)
        meals.append(meal)

    return render_template('cart.html', meals=meals, form=form)


@app.route('/addtocart/<int:meal>/')
def addtochart(meal):
    price = db.session.query(MealModel).get(meal).price
    session['cart_id'] = session.get('cart_id', [])
    session['cart_price'] = session.get('cart_price', [])
    session['cart_id'].append(str(meal))
    session['cart_price'].append(price)
    return redirect('/cart/')


@app.route('/delfromcart/<meal>/')
def delfromcart(meal):
    idx = session['cart_id'].index(meal)
    session['cart_id'].pop(idx)
    session['cart_price'].pop(idx)
    flash('Блюдо удалено из корзины')
    return redirect('/cart/')

@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


@app.route('/account/')
def account():
    if session['user_id']:
        user = db.session.query(UserModel).get(session['user_id'])
        return render_template('account.html', orders=user.orders)
    return abort(404, 'Вы не авторизированы для доступа к этой странице. Необходимо пройти регистрацию')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = UserModel.query.filter_by(email=form.email.data).first()
        # Если такой пользователь существует
        if user and user.role in ['authorized_user', 'admin']:
            # Не можем зарегистрировать, так как пользователь уже существует
            error_msg = "Пользователь с указанным e-mail уже существует"
            return render_template("register.html", error_msg=error_msg, form=form)

        elif user and user.role == 'guest':
            try:
                form.populate_obj(user)
                user.role = 'authorized_user'
                db.session.add(user)
                db.session.commit()
            except Exception as er:
                return render_template('register.html', form=form)
            flash(
                'С возвращением! Теперь вы имеете статус зарегистрированного пользователя. Ваша история заказов доступа в личном кабинете.')
            session['user_id'] = user.id
            return redirect('/account/')

        user = UserModel()
        try:
            form.populate_obj(user)
            user.role = 'authorized_user'
            db.session.add(user)
            db.session.commit()
        except Exception as er:
            return render_template('register.html', form=form)
        flash('Поздравляем, вы успешно зарегистровались! Добро пожаловать в личный кабинет пользователя.')
        session['user_id'] = user.id
        return redirect('/account/')
    return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    session['is_auth'] = False
    session['user_id'] = None
    session['cart_id'] = []
    session['cart_price'] = []

    return render_template('logout.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_msg = ""
    if form.validate_on_submit():
        user = db.session.query(UserModel).filter(UserModel.email == form.email.data).first()
        if user and form.password.data == user.password:
            flash('И снова здравствуйте! Добро пожаловать в личный кабинет заказа блюд.')
            print(user, user.password)
            session['user_id'] = user.id
            return redirect('/account/')
        error_msg = "Неверный email или пароль."
    return render_template('auth.html', form=form, error_msg=error_msg)

@app.errorhandler(404)
def no_auth(error):
    return (error)
