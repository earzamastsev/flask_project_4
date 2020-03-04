from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# meals_categories_association = db.Table('meals_categories', \
#                                         db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')), \
#                                         db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
#                                         )


class MealModel(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    picture = db.Column(db.String(128), nullable=False)
    category = db.relationship('CategoryModel', back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    meals = db.relationship('MealModel', back_populates='category')
