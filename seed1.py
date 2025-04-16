from app import app, db, User, FoodItem, Order

with app.app_context():
    # Add a sample consumer
    consumer = User(
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@example.com",
        password="hashed_password",
        city="New York",
        address="123 Main St",
        is_homemaker=False
    )
    db.session.add(consumer)
    db.session.commit()

    # Add sample food items
    food_item1 = FoodItem(
        name="Spaghetti Bolognese",
        location="New York",
        price=12.99,
        rating=4.5,
        description="Classic Italian pasta with rich meat sauce.",
        image="spaghetti.jpg",
        homemaker_id=1  # Replace with a valid homemaker ID
    )
    db.session.add(food_item1)
    db.session.commit()

print("Sample orders added successfully!")
