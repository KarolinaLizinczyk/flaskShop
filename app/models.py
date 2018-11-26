from app import db
from flask_login import UserMixin



# Creating db for User Registration
class ShopUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True)
    last_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(20), unique=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class ShopProduct(db.Model):
    __tablename__ = 'products'
    __searchable__ = ['sku', 'name', 'category']
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(2), nullable=True)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    discount = db.Column(db.Integer, nullable=True)

    def __init__(self, sku, name, category, description, price, quantity, image_filename, image_url, discount):
        self.sku = sku
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.quantity = quantity
        self.image_filename = image_filename
        self.image_url = image_url
        self.discount = discount

    def __unicode__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    product_sku = db.Column(db.String(255))
    buyer_name = db.Column(db.String(40), nullable=True)
    buyer_surname = db.Column(db.String(40), nullable=True)
    buyer_email = db.Column(db.String(50), nullable=True)
    buyer_phone = db.Column(db.String(15), nullable=True)
    buyer_address = db.Column(db.String(50), nullable=True)
    buyer_zipcode = db.Column(db.String(15), nullable=True)
    buyer_city = db.Column(db.String(15), nullable=True)
    payment_option = db.Column(db.String(30), nullable=True)
    shipment_option = db.Column(db.String(30), nullable=True)
    checkout = db.Column(db.Boolean, nullable=True, default=False)
    total_price = db.Column(db.Numeric(2), nullable=True)
    order_number = db.Column(db.Integer, nullable=True)

    def __init__(self, product_sku, buyer_name, buyer_surname, buyer_email, buyer_phone, buyer_address, buyer_zipcode,
                 buyer_city, payment_option, shipment_option, checkout, total_price, order_number):
        self.product_sku = product_sku
        self.buyer_name = buyer_name
        self.buyer_surname = buyer_surname
        self.buyer_email = buyer_email
        self.buyer_phone = buyer_phone
        self.buyer_address = buyer_address
        self.buyer_zipcode = buyer_zipcode
        self.buyer_city = buyer_city
        self.payment_option = payment_option
        self.shipment_option = shipment_option
        self.checkout = checkout
        self.total_price = total_price
        self.order_number = order_number