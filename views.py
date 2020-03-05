from flask import session, request, render_template, abort, flash, redirect
from models import MealModel, CategoryModel, UserModel
from sqlalchemy.sql.expression import func
from app import app, db
from forms import RegisterForm


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


@app.route('/cart/')
def cart():
    meals = []
    for meal in session['cart_id']:
        meal = db.session.query(MealModel).get(meal)
        meals.append(meal)
    return render_template('cart.html', meals=meals)


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
    return render_template('account.html')


@app.route('/login/')
def login():
    session['is_auth'] = True
    return render_template('auth.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel()
        try:
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
        except Exception as er:
            return render_template('register.html', form=form)
        flash('Поздравляем, вы успешно зарегистровались! Добро пожаловать в личный кабинет пользователя.')
        session['is_auth'] = True
        return redirect('/account/')
    return render_template('register.html', form=form)


@app.route('/logout/')
def logout():
    session['is_auth'] = False
    return render_template('logout.html')
