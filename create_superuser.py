from app import db, User, create_app  # Import your Flask app factory function

def create_superuser():
    # Check if an admin user already exists
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        # Create a new admin user
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('adminpass')  # Set the admin password here
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    app = create_app()  # Create the Flask app instance
    with app.app_context():  # Push the application context
        create_superuser()
