from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Change to your db URI if needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Import and register blueprints here if needed
    # from .routes import main
    # app.register_blueprint(main)

    return app

app = create_app()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='customer', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), default='default.jpg')
    stock = db.Column(db.Integer, default=0)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    complete = db.Column(db.Boolean, default=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    @property
    def total(self):
        return sum(item.product.price * item.quantity for item in self.items)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

# Routes
@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if user_exists:
            flash('Username or email already exists.')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if not g.user:
        return redirect(url_for('login'))
    
    # Get active order (cart) or create new one
    order = Order.query.filter_by(user_id=g.user.id, complete=False).first()
    if not order:
        order = Order(user_id=g.user.id)
        db.session.add(order)
        db.session.commit()
    
    return render_template('cart.html', order=order)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not g.user:
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    # Get active order (cart) or create new one
    order = Order.query.filter_by(user_id=g.user.id, complete=False).first()
    if not order:
        order = Order(user_id=g.user.id)
        db.session.add(order)
        db.session.commit()
    
    # Check if item already in cart
    order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()
    if order_item:
        order_item.quantity += quantity
    else:
        order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_item)
    
    db.session.commit()
    flash(f'Added {product.name} to your cart.')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    if not g.user:
        return redirect(url_for('login'))
    
    order_item = OrderItem.query.get_or_404(item_id)
    # Ensure the item belongs to the user's order
    if order_item.order.user_id != g.user.id:
        flash('Access denied.')
        return redirect(url_for('cart'))
    
    db.session.delete(order_item)
    db.session.commit()
    flash('Item removed from cart.')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if not g.user:
        return redirect(url_for('login'))
    
    order = Order.query.filter_by(user_id=g.user.id, complete=False).first()
    if not order or not order.items:
        flash('Your cart is empty.')
        return redirect(url_for('cart'))
    
    return render_template('checkout.html', order=order)

@app.route('/place_order', methods=['POST'])
def place_order():
    if not g.user:
        return redirect(url_for('login'))
    
    order = Order.query.filter_by(user_id=g.user.id, complete=False).first()
    if not order or not order.items:
        flash('Your cart is empty.')
        return redirect(url_for('cart'))
    
    # Here you would typically handle payment processing
    # For this example, we'll just mark the order as complete
    
    order.complete = True
    db.session.commit()
    
    flash('Your order has been placed successfully!')
    return redirect(url_for('order_confirmation', order_id=order.id))

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    if not g.user:
        return redirect(url_for('login'))
    
    order = Order.query.get_or_404(order_id)
    if order.user_id != g.user.id:
        flash('Access denied.')
        return redirect(url_for('home'))
    
    return render_template('order_confirmation.html', order=order)

# Admin Routes
@app.route('/admin')
def admin():
    if not g.user or not g.user.is_admin:
        flash('Access denied.')
        return redirect(url_for('home'))
    
    products = Product.query.all()
    orders = Order.query.filter_by(complete=True).all()
    users = User.query.all()
    
    return render_template('admin/dashboard.html', products=products, orders=orders, users=users)

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if not g.user or not g.user.is_admin:
        flash('Access denied.')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        
        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!')
        return redirect(url_for('admin'))
    
    return render_template('admin/add_product.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is created
        # Check if the superuser already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('adminpass')  # Set the superuser password
            db.session.add(admin)
            db.session.commit()
            print("Superuser account created successfully!")
        else:
            print("Superuser already exists.")
    
    app.run(debug=True)
