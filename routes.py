from extension import app, db
from flask import render_template, request, redirect, send_from_directory, url_for
from forms import AddProduct, RegisterForm, LoginForm
from models import Product, Category, User, CartItem, Sale
from flask_login import logout_user, login_user, current_user, login_required
import os


@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/delete/<int:id>")
def delete_product(id):
    current = Product.query.get(id)
    db.session.delete(current)
    db.session.commit()
    return redirect("/")



@app.route('/detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    sales = Sale.query.filter_by(product_id=product.id).all()
    return render_template('detail.html', product=product, sales=sales)


@app.route('/delete_sale/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return "Sale not found"
    db.session.delete(sale)
    db.session.commit()
    return redirect(url_for('product_detail', product_id=sale.product_id))


@app.route("/uploadfile", methods=["GET", "POST"])
def upload_file():
    form = AddProduct()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    obj = Product(name=form.name.data,
    file=filename,
    price = form.price.data)
    db.session.add(obj)
    db.session.commit()

    return redirect("/")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@login_required
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(product_id=product_id, user_id=current_user.id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return redirect("/")


@login_required
@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_price = 0
        products = []
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            product.quantity = cart_item.quantity
            total_price += product.price * cart_item.quantity
            products.append(product)
        return render_template('cart.html', products=products, total_price=total_price, cart_items=cart_items)
    else:
        return redirect(url_for('login'))



@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart'))




@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    form = AddProduct()
    form.category.choices=[(category.id, category.name) for category in Category.query.all()]
    category = Category.query.get(form.category.data)
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            obj = Product(name=form.name.data,
                          file= filename,
                          price = form.price.data,
                          category= category)
            db.session.add(obj)
            db.session.commit()
            return redirect("/")
    return render_template("addproduct.html", form=form)

@app.route('/add_sale/<int:product_id>', methods=['GET', 'POST'])
def add_sale(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        discount_percentage = float(request.form.get('discount_percentage', 0))
        if discount_percentage > 0:
            product.price *= (1 - discount_percentage / 100)
            db.session.commit()
            return redirect(url_for('product_detail', product_id=product_id))

    return render_template('sale.html', product=product)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        exists = User.query.filter(User.username==form.username.data).first()
        if exists and exists.password == form.password.data:
            login_user(exists)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/category/<int:category_id>")
def category_select(category_id):
    current_category = Category.query.get(category_id)
    products = current_category.product_id
    return render_template("index.html", products=products)

@app.route('/search')
def search():
    query = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('index.html', products=products, query=query)

