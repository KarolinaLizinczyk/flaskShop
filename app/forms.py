from flask_wtf import Form
from wtforms import StringField, validators, TextAreaField, DecimalField, IntegerField, FileField, PasswordField, BooleanField
from flask_wtf.file import FileRequired


class AddItemForm(Form):
    sku = IntegerField('SKU', [validators.input_required()])
    name = StringField('Product Name', [validators.input_required(), validators.Length(min=4, max=25)])
    category = StringField('Category', [validators.input_required(), validators.Length(min=6, max=15)])
    description = TextAreaField('Product Description', [validators.input_required(), validators.Length(min=30)])
    price = DecimalField('Price', [validators.input_required()])
    quantity = IntegerField('Quantity', [validators.input_required()])
    image = FileField('Image', validators=[FileRequired()])
    discount = IntegerField('Discount', [validators.input_required(), validators.Length(max=3)])


class ContactForm(Form):
    email = StringField('Your Email Address', [validators.input_required(), validators.email(), validators.Length(min=6, max=35)])
    title = StringField('Title', [validators.input_required(), validators.Length(min=4, max=25)])
    content = TextAreaField('Content', [validators.input_required(), validators.Length(min=30)])


class ShippingForm(Form):
    name = StringField('First Name', [validators.input_required(), validators.Length(min=4, max=25)])
    surname = StringField('Surname', [validators.input_required(), validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.input_required(), validators.email(), validators.Length(min=6, max=35)])
    phone_number = IntegerField('Phone Number', [validators.input_required(), validators.Length(max=9)])
    address = StringField('Address', [validators.input_required(), validators.Length(min=5, max=35)])
    zip_code = StringField('Zipcode', [validators.input_required(), validators.Length(max=6)])
    city = StringField('City', [validators.input_required(), validators.Length(min=4, max=15)])


class UserForm(Form):
    first_name = StringField('First Name', [validators.input_required(), validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.input_required(), validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.input_required(), validators.email(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
                             validators.input_required(),
                             validators.DataRequired(),
                             validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
