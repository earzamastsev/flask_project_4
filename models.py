from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

meals_orders_association = db.Table('meals_orders', \
                                    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')), \
                                    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'))
                                    )


class MealModel(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    picture = db.Column(db.String(128), nullable=False)
    category = db.relationship('CategoryModel', back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    orders = db.relationship('OrderModel', secondary=meals_orders_association, back_populates='meals')


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    meals = db.relationship('MealModel', back_populates='category')


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    orders = db.relationship('OrderModel', back_populates='users')


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    summa = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel', back_populates='orders')
    meals = db.relationship('MealModel', secondary=meals_orders_association, back_populates='orders')
