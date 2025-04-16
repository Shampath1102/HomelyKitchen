from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homely_kitchen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------
# Database Models
# ---------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    is_homemaker = db.Column(db.Boolean, default=False)
    # Additional fields can be added as needed

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    homemaker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add foreign key to User if needed (e.g., cook_id)
    homemaker = db.relationship('User', backref='food_items', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Relationships
    consumer = db.relationship('User', backref='orders', lazy=True)
    food_item = db.relationship('FoodItem', backref='orders', lazy=True)


# ---------------------
# Routes
# ---------------------

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Consumer Signup
@app.route('/consumer_signup', methods=['GET', 'POST'])
def consumer_signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        address = request.form['address']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('consumer_signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            city=city,
            address=address,
            is_homemaker=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('consumer_login'))
    return render_template('consumer_signup.html')

# Consumer Login
@app.route('/consumer_login', methods=['GET', 'POST'])
def consumer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, is_homemaker=False).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_homemaker'] = user.is_homemaker
            flash('Logged in successfully!', 'success')
            return redirect(url_for('consumer_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('consumer_login'))
    return render_template('consumer_login.html')

# Homemaker Signup
@app.route('/homemaker_signup', methods=['GET', 'POST'])
def homemaker_signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        address = request.form['address']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('homemaker_signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            city=city,
            address=address,
            is_homemaker=True
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('homemaker_login'))
    return render_template('homemaker_signup.html')

# Homemaker Login
@app.route('/homemaker_login', methods=['GET', 'POST'])
def homemaker_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, is_homemaker=True).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_homemaker'] = user.is_homemaker
            flash('Logged in successfully!', 'success')
            return redirect(url_for('homemaker_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('homemaker_login'))
    return render_template('homemaker_login.html')

# Consumer Home Page
@app.route('/consumer_home')
def consumer_home():
    if 'user_id' not in session or session.get('is_homemaker'):
        flash('Access denied. Please log in as a consumer.', 'danger')
        return redirect(url_for('consumer_login'))
    food_items = FoodItem.query.all()
    return render_template('consumer_home.html', food_items=food_items)

# Food Detail Page
@app.route('/food_detail/<int:food_id>')
def food_detail(food_id):
    if 'user_id' not in session or session.get('is_homemaker'):
        flash('Access denied. Please log in as a consumer.', 'danger')
        return redirect(url_for('consumer_login'))
    food = FoodItem.query.get_or_404(food_id)
    return render_template('food_detail.html', food=food)

# Order Food
@app.route('/order_food/<int:food_id>', methods=['POST'])
def order_food(food_id):
    if 'user_id' not in session or session.get('is_homemaker'):
        flash('Access denied. Please log in as a consumer.', 'danger')
        return redirect(url_for('consumer_login'))

    # Fetch the food item
    food_item = FoodItem.query.get_or_404(food_id)

    # Get quantity from the form
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if no quantity is provided
    if quantity < 1:
        flash('Quantity must be at least 1.', 'danger')
        return redirect(url_for('food_detail', food_id=food_id))

    # Calculate the total price
    total_price = food_item.price * quantity

    # Save the order to the database
    new_order = Order(
        consumer_id=session['user_id'],
        food_item_id=food_id,
        quantity=quantity,
        total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()

    flash('Order placed successfully!', 'success')
    return redirect(url_for('consumer_home'))


# Search Food Items
@app.route('/search_food', methods=['GET'])
def search_food():
    if 'user_id' not in session or session.get('is_homemaker'):
        flash('Access denied. Please log in as a consumer.', 'danger')
        return redirect(url_for('consumer_login'))
    query = request.args.get('query', '')
    food_items = FoodItem.query.filter(FoodItem.name.ilike(f'%{query}%')).all()
    return render_template('consumer_home.html', food_items=food_items)

# Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'danger')
        return redirect(url_for('index'))
    user = User.query.get_or_404(session['user_id'])
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.city = request.form['city']
        user.address = request.form['address']
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('consumer_home'))
    return render_template('profile.html', user=user)

@app.route('/homemaker_dashboard')
def homemaker_dashboard():
    if 'user_id' not in session or not session.get('is_homemaker'):
        flash('Access denied. Please log in as a homemaker.', 'danger')
        return redirect(url_for('homemaker_login'))

    homemaker_id = session['user_id']

    # Fetch food items created by this homemaker
    food_items = FoodItem.query.filter_by(homemaker_id=homemaker_id).all()

    # Fetch orders related to these food items
    food_item_ids = [item.id for item in food_items]
    orders = Order.query.filter(Order.food_item_id.in_(food_item_ids)).all()

    return render_template('homemaker_dashboard.html', food_items=food_items, orders=orders)


@app.route('/add_food_item', methods=['GET', 'POST'])
def add_food_item():
    if 'user_id' not in session or not session.get('is_homemaker'):
        flash('Access denied. Please log in as a homemaker.', 'danger')
        return redirect(url_for('homemaker_login'))

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price = request.form['price']
        rating = request.form['rating']
        description = request.form['description']
        image = request.form['image']

        # Save the food item with homemaker_id
        homemaker_id = session['user_id']
        new_food = FoodItem(
            name=name,
            location=location,
            price=float(price),
            rating=float(rating),
            description=description,
            image=image,
            homemaker_id=homemaker_id
        )
        db.session.add(new_food)
        db.session.commit()

        flash('Food item added successfully!', 'success')
        return redirect(url_for('homemaker_dashboard'))

    return render_template('add_food_item.html')
@app.route('/edit_food_item/<int:food_id>', methods=['GET', 'POST'])
def edit_food_item(food_id):
    # Check if the user is logged in and is a homemaker
    if 'user_id' not in session or not session.get('is_homemaker'):
        flash('Access denied. Please log in as a homemaker.', 'danger')
        return redirect(url_for('homemaker_login'))

    # Fetch the food item by ID
    food_item = FoodItem.query.get_or_404(food_id)

    if request.method == 'POST':
        # Update the food item details
        food_item.name = request.form['name']
        food_item.location = request.form['location']
        food_item.price = float(request.form['price'])
        food_item.rating = float(request.form['rating'])
        food_item.description = request.form['description']
        food_item.image = request.form['image']

        db.session.commit()
        flash('Food item updated successfully!', 'success')
        return redirect(url_for('homemaker_dashboard'))

    # Render the edit form
    return render_template('edit_food_item.html', food_item=food_item)


@app.route('/delete_food_item/<int:food_id>', methods=['POST'])
def delete_food_item(food_id):
    # Check if the user is logged in and is a homemaker
    if 'user_id' not in session or not session.get('is_homemaker'):
        flash('Access denied. Please log in as a homemaker.', 'danger')
        return redirect(url_for('homemaker_login'))

    # Fetch the food item by ID
    food_item = FoodItem.query.get_or_404(food_id)

    # Ensure the logged-in homemaker owns the food item
    if food_item.homemaker_id != session['user_id']:
        flash('You are not authorized to delete this food item.', 'danger')
        return redirect(url_for('homemaker_dashboard'))

    # Delete the food item from the database
    db.session.delete(food_item)
    db.session.commit()

    flash('Food item deleted successfully!', 'success')
    return redirect(url_for('homemaker_dashboard'))


@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session:
        flash('Please log in to update orders.', 'danger')
        return redirect(url_for('login'))  # Replace 'login' with the appropriate login route

    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status', 'Pending')  # Default to 'Pending' if no status is provided

    order.status = new_status
    db.session.commit()

    flash(f'Order {order.id} status updated to {new_status}.', 'success')
    return redirect(url_for('delivery_orders'))

@app.route('/delivery_orders')
def delivery_orders():
    if 'user_id' not in session:
        flash('Please log in to view orders.', 'danger')
        return redirect(url_for('login'))  # Replace 'login' with the appropriate login route

    orders = Order.query.order_by(Order.timestamp.desc()).all()  # Fetch all orders sorted by timestamp
    return render_template('delivery_orders.html', orders=orders)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))



# ---------------------
# Initialize Database with Sample Data
# ---------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)