from app import app
from extension import db, app, login_manager
from flask_login import UserMixin
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


def __str__(self):
    return f"{self.name}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    product_id = db.relationship('Product', backref='category', lazy=True)

def __str__(self):
    return f"{self.name}"

# Association table for the many-to-many relationship
cartitem_product_association = db.Table(
'cartitem_product_association',
db.Column('cartitem_id', db.Integer, db.ForeignKey('cart_item.id')),
db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
db.Column('quantity', db.Integer, nullable=False, default=1)
)

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')


def __str__(self):
    return f"{self.user_id}"

class User(db.Model, UserMixin):
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

def __init__(self, username, password, role="guest"):
    self.username = username
    self.password = password
    self.role = role


class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Sale {self.id}: ${self.sale_price} on {self.sale_date}>'



def __str__(self):
    return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

        vegetables_fruit = Category(name="vegetables & fruit")
        meat_fish = Category(name="Meat & Fish")
        Bread_Bakery = Category(name="Bread & Bakery")
        Beauty_Health = Category(name="Beauty & Health")

        user = User(username = "admin", password= "1234", role="admin")

        db.session.add_all([vegetables_fruit, meat_fish, Bread_Bakery, Beauty_Health, user])
        db.session.commit()