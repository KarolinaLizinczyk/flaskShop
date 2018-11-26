from app import app, login_manager, db, images
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import  login_user, logout_user, login_required
from flask_mail import Mail, Message
from decimal import Decimal
from random import randint
from app.forms import AddItemForm, ContactForm, ShippingForm, UserForm
from app.models import ShopUser, ShopProduct, Order


# Index Page
@app.route('/')
def index_shop():
    if 'cart' in session:
        session['cart_count'] = len(session['cart'])
    else:
        session['cart_count'] = 0

    page = request.args.get('page', 1, type=int)
    all_products = ShopProduct.query.order_by(ShopProduct.id.desc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)


    return render_template('index_shop.html', all_products=all_products)


# Registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    user_form = UserForm(request.form)
    if request.method == 'POST' and user_form.validate():
        user = ShopUser(request.form['first_name'], request.form['last_name'], request.form['email'],
                        request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return render_template('registration.html', user_form=user_form)
    return render_template('registration.html', user_form=user_form)


# loginManager
@login_manager.user_loader
def load_user(id):
    return ShopUser.query.get(int(id))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = UserForm(request.form)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = ShopUser.query.filter_by(email=email).first()
        user_password = ShopUser.query.filter_by(password=password).first()

        if not user:
            flash('User not found')
        elif not user_password:
            flash('Password is incorrect')
        login_user(user)
        session['logged_in'] = True
        flash('You are now logged in')
        return render_template('login.html', login_form=login_form)

    return render_template('login.html', login_form=login_form)


# Logout
@app.route('/logged_out')
@login_required
def logged_out():
    logout_user()
    session.clear()
    flash('You are now logged out')
    return redirect(url_for('login'))


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Privacy Policy
@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


# Store Rules
@app.route('/store_rules')
def store_rules():
    return render_template('store_rules.html')


# Sale
@app.route('/sale', defaults={'page': 1}, methods=['GET'])
@app.route('/sale/<int:page>')
def sale(page=1):
    sale_items = ShopProduct.query.filter(ShopProduct.discount != 0).order_by(ShopProduct.id.desc()).paginate(page, 1,
                                                                                                              False)
    print(sale_items)
    return render_template('sale.html', all_items=sale_items)


# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm(request.form)
    if request.method == 'POST':
        msg = Message(sender='someone@gmail.com', recipients=['lizinczyk.karolina@gmail.com'])
        msg.subject = "Message from your visitor"
        msg.body = """
            From: %s <%s>,
            %s
        """ % (contact_form.email.data, contact_form.title.data, contact_form.content.data)
        Mail.send(msg)
        flash("Thank you for your message. We'll get back to you shortly.")
        return render_template('contact.html', contact_form=contact_form)
    return render_template('contact.html', contact_form=contact_form)


# ADD TO CART
@app.route('/shop_item/<string:sku>', methods=['GET', 'POST'])
def shop_item(sku):
    item = ShopProduct.query.filter_by(sku=sku).first()

    if request.method == 'POST':
        if "cart" not in session:
            session["cart"] = []
        session["cart"].append(sku)
        flash("Successfully added to cart!")
        return redirect(url_for("cart"))

    return render_template('shop_item.html', item=item)


# CART
@app.route('/cart')
def cart():
    if "cart" not in session or session['cart'] == []:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart={}, total=0, success=True)
    else:
        session['cart_count'] = len(session['cart'])
        items = session["cart"]
        dict_of_products = {}
        print(items)
        total_price = 0
        total_qty = 0
        for item in items:
            product = ShopProduct.query.filter_by(sku=item).first()
            if product.discount:
                total_price += (product.price * product.discount) / 100
            else:
                total_price += product.price
            total_qty += 1
            if product.sku in dict_of_products:
                dict_of_products[product.sku]["quantity"] += 1
            else:
                dict_of_products[product.sku] = {"quantity": 1, "name": product.name, "price": product.price,
                                                 "sku": product.sku, "discount": product.discount, "image_url": product.image_url, "image_filename": product.image_filename}

        return render_template('cart.html', display_cart=dict_of_products, total=total_price, product=product,
                               total_qty=total_qty)


# CHECKOUT
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    shipping_form = ShippingForm(request.form)
    if request.method == 'POST':
        items_list = session['cart']
        items_to_str = ",".join(str(item) for item in items_list)

        random_order_number = randint(0, 500000)

        buyer_details = Order(items_to_str, request.form['name'], request.form['surname'], request.form['email'],
                              request.form['phone_number'], request.form['address'], request.form['zip_code'],
                              request.form['city'], "", 0, False, 0, random_order_number)
        db.session.add(buyer_details)
        db.session.commit()

        session['order_id'] = buyer_details.id

        return redirect(url_for('checkout2'))
    return render_template('checkout.html', shipping_form=shipping_form)


# CHECKOUT2
@app.route('/checkout2', methods=['GET', 'POST'])
def checkout2():
    if request.method == 'POST':
        Order.query.filter_by(id=session['order_id']).update(dict(payment_option=request.form['select_payment_option'],
                                                                  shipment_option=request.form[
                                                                      'select_shipment_option']))
        db.session.commit()
        return redirect(url_for('checkout3'))
    return render_template('checkout2.html')


# CHECKOUT3
@app.route('/checkout3', methods=['GET', 'POST'])
def checkout3():
    id = session['order_id']

    order = Order.query.filter_by(id=id).first()
    order_num = order.order_number

    # Sku List spit
    temp = order.product_sku
    items = temp.split(",")

    # Converting Shipment Option to Decimal
    shipment = order.shipment_option
    option_ss = shipment.split(" ")
    option_ss_to_int = option_ss[2]
    decimal_ss = Decimal(option_ss_to_int)

    # Converting Payment Option to Decimal
    payment = order.payment_option
    option_pp = payment.split(" ")
    if payment == "Payment on delivery 5.00":
        option_pp_to_int = option_pp[3]
        decimal_pp = Decimal(option_pp_to_int)

    else:
        option_pp_to_int = option_pp[1]
        decimal_pp = Decimal(option_pp_to_int)

    # Retrieving data from db
    dict_of_products = {}
    total_price = 0
    total_qty = 0
    index_count = 1
    for index, item in enumerate(items):
        product = ShopProduct.query.filter_by(sku=item).first()
        if product.discount:
            total_price += (product.price * product.discount) / 100
        else:
            total_price += product.price
        total_qty += 1
        if product.sku in dict_of_products:
            dict_of_products[product.sku]["quantity"] += 1
        else:
            dict_of_products[product.sku] = {"quantity": 1, "name": product.name, "price": product.price,
                                             "sku": product.sku, "discount": product.discount}
            index_count += index

    print(index_count)
    my_price = total_price + decimal_pp + decimal_ss
    print(my_price)
    if request.method == 'POST':

        myProductsString = """
            Hello {0}!
            <br>
            <br>
            Thank you for the order, number {1}
            <hr>
            Ordered Products:
            <br>
            <br>
            <table border="1" style="width:85%">
                <tr>
                    <th>PN</th>
                    <th>Order ID</th>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                </tr>
        """.format(order.buyer_name, order.order_number)

        NP = 1
        for key, value in dict_of_products.iteritems():
            if value['discount']:
                myProductsString += """
                    <tr>
                    <td><center>{0}</td>
                    <td><center>{1}</td>
                    <td><center>{2}</td>
                    <td><center>{3}</td>
                    <td><center>{4}</td>
                    </tr>
                    """.format(NP,order.order_number, value['name'], value['quantity'], ((value['price'] * value['discount'])/100))
            else:
                myProductsString += """
                    <tr>
                    <td><center>{0}</td>
                    <td><center>{1}</td>
                    <td><center>{2}</td>
                    <td><center>{3}</td>
                    <td><center>{4}</td>
                    </tr>
                    """.format(NP,order.order_number, value['name'], value['quantity'], value['price'])
            NP += 1

        myProductsString += """

            </table>
            <br>
            Total Price: ${0}
            <br>
            <hr>
            Buyer Details:<br>
            <br>
            {1} {2}<br>
            {3} <br>
            {4} {5}<br>
            {6}<br>
            {7}
            <p>&nbsp</p>
            <hr>
            <br>
            Regards,<br>
            Owl Shop Team
        """.format(my_price, order.buyer_name, order.buyer_surname,
                   order.buyer_address, order.buyer_zipcode, order.buyer_city, order.buyer_email,
                   order.buyer_phone)

        email = order.buyer_email
        msg = Message("Your order confirmation", recipients=[email])
        msg.sender = 'Owl Shop <lizinczyk.karolina@gmail.com>'
        msg.html = myProductsString
        Mail.send(msg)


        print (myProductsString)
        flash('Your request has been completed successfully. Thank you for the shopping')
        session['cart'] = []
        session['cart_count'] = 0

        Order.query.filter_by(id=session['order_id']).update(dict(total_price=my_price, checkout=True))
        db.session.commit()
        order_num = order.order_number
        return render_template('checkout3.html', order=order, display_cart=dict_of_products, total=total_price,
                               decimal_ss=decimal_ss, decimal_pp=decimal_pp, success=True, order_number=order_num)
    return render_template('checkout3.html', order=order, display_cart=dict_of_products, total=total_price,
                           decimal_ss=decimal_ss, decimal_pp=decimal_pp, success=False, order_number=order_num)


# ORDERS
@app.route('/orders')
def orders():
    all_orders = [u.__dict__ for u in Order.query.all()]

    if all_orders > 0:
        return render_template('orders.html', all_orders=all_orders)
    else:
        msg = "No orders Found"
        return render_template('orders.html', msg=msg)
    return render_template('orders.html')


# ADD SHOP ITEM TO DB
@app.route('/add_shop_item', methods=['GET', 'POST'])
def add_shop_item():
    add_item_form = AddItemForm(request.form)
    if request.method == 'POST':

        filename = images.save(request.files['image'])
        url = images.url(filename)
        add_item = ShopProduct(request.form['sku'], request.form['name'], request.form['category'],
                               request.form['description'], request.form['price'], request.form['quantity'],
                               filename, url, request.form['discount'])
        db.session.add(add_item)
        db.session.commit()
        flash('Item saved. Thank you')
        return render_template('add_shop_item.html', add_item_form=add_item_form)

    return render_template('add_shop_item.html', add_item_form=add_item_form)


# DELETE SHOP ITEM FROM DB
@app.route('/delete_shop_item/<sku>', methods=['POST'])
def delete_shop_item(sku):
    if session["cart"] == []:
        return redirect(url_for('cart'))
    else:
        session["cart"].remove(sku)
        flash('Product Deleted successfully')
        return redirect(url_for('cart'))


# STORAGE
@app.route('/items_storage')
def items_storage():
    items = [u.__dict__ for u in ShopProduct.query.all()]
    if items > 0:
        return render_template('items_storage.html', items=items)
    else:
        msg = 'No articles Found'
        return render_template('items_storage.html', msg=msg)


# ITEM UPDATE
@app.route('/edit_item/<sku>', methods=['GET', 'POST'])
def edit_item(sku):
    product = ShopProduct.query.filter_by(sku=sku).first()
    form = AddItemForm()

    form.sku.data = product.sku
    form.name.data = product.name
    form.category.data = product.category
    form.description.data = product.description
    form.price.data = product.price
    form.quantity.data = product.quantity
    form.discount.data = product.discount

    if request.method == 'POST':
        ShopProduct.query.filter_by(sku=sku).update(
            dict(sku=request.form['sku'], name=request.form['name'], category=request.form['category'],
                 description=request.form['description'], quantity=request.form['quantity'],
                 price=request.form['price'],
                 discount=request.form['discount']))
        db.session.commit()
        flash('Item Updated successfully')
        return render_template('edit_item.html', form=form, product=product)
    return render_template('edit_item.html', form=form, product=product)


# DELETE ITEM
@app.route('/delete_item/<sku>', methods=['POST'])
def delete_item(sku):
    ShopProduct.query.filter_by(sku=sku).delete()
    db.session.commit()
    flash('Product Deleted successfully')
    return redirect(url_for('items_storage'))


# DELETE ITEM
@app.route('/delete_order/<id>', methods=['POST'])
def delete_order(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Product Released successfully')
    return redirect(url_for('orders'))


# PRODUCT CATEGORY
@app.route('/all_items', methods=['GET'])
@app.route('/all_items/<int:page>')
def all_items(page=1):
    all_products = ShopProduct.query.order_by(ShopProduct.id.desc()).paginate(page, per_page=6, error_out=False)
    return render_template('all_items.html', all_products=all_products)


# RESULTS FROM SEARCH ENGINE
@app.route('/search_results')
def search_results():
    products = ShopProduct.query.whoosh_search(request.args.get('query')).all()
    return render_template('/search_results.html', products=products)


@app.context_processor
def to_decimal_filter():
    def format_price(amount, currency=u'$'):
        return u'{0:.2f}{1}'.format(amount, currency)

    return dict(format_price=format_price)