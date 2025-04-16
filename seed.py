from app import app, db, User, FoodItem

with app.app_context():
    # Clear the database (optional)
    db.drop_all()
    db.create_all()

    # Add homemakers
    homemaker1 = User(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        password="hashed_password",  # Hash passwords in real apps
        city="San Francisco",
        address="456 Elm St",
        is_homemaker=True
    )
    homemaker2 = User(
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        password="hashed_password",
        city="Los Angeles",
        address="789 Oak Ave",
        is_homemaker=True
    )

    # Add a consumer
    consumer = User(
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@example.com",
        password="hashed_password",
        city="New York",
        address="123 Main St",
        is_homemaker=False
    )

    db.session.add_all([homemaker1, homemaker2, consumer])
    db.session.commit()

    # Add food items associated with homemakers
    food1 = FoodItem(
        name="Spaghetti Bolognese",
        location="New York",
        price=12.99,
        rating=4.5,
        description="Classic Italian pasta with rich meat sauce.",
        image="spaghetti.jpg",
        homemaker_id=homemaker1.id
    )
    food2 = FoodItem(
        name="Chicken Curry",
        location="Los Angeles",
        price=10.50,
        rating=4.7,
        description="Traditional Indian chicken curry with spices.",
        image="chicken_curry.jpg",
        homemaker_id=homemaker2.id
    )
    food3 = FoodItem(
        name="Vegan Buddha Bowl",
        location="San Francisco",
        price=15.00,
        rating=4.8,
        description="Fresh vegetables with quinoa and hummus.",
        image="buddha_bowl.jpg",
        homemaker_id=homemaker1.id
    )
    food4 = FoodItem(
        name="Classic Cheeseburger",
        location="Los Angeles",
        price=8.99,
        rating=4.2,
        description="Grilled beef patty with cheese and lettuce.",
        image="cheeseburger.jpg",
        homemaker_id=homemaker2.id
    )

    db.session.add_all([food1, food2, food3, food4])
    db.session.commit()

print("Database seeded successfully!")
