Here’s a sample documentation for your Flask-based eCommerce project:

---

# **E-Commerce Flask Application Documentation**

## **Overview**

This is a simple e-commerce application built using Flask and SQLite. It allows users to browse products, register, log in, add products to their cart, and place orders. Admins can manage the products, view orders, and create new products via an admin dashboard.

---

## **Features**

- **User Authentication**: Users can register, log in, and log out. Passwords are hashed for security.
- **Product Management**: Users can view products, their details, and add them to their cart.
- **Shopping Cart**: Users can add, remove, and view items in their cart.
- **Order Management**: Users can place an order, and the admin can view completed orders.
- **Admin Dashboard**: Admins can add, update, or delete products and view orders.

---

## **Technologies Used**

- **Python**: The backend language used for the application.
- **Flask**: A lightweight web framework used for the application.
- **SQLAlchemy**: An ORM (Object Relational Mapper) used to interact with the SQLite database.
- **SQLite**: A lightweight, serverless database used to store user, product, and order data.
- **HTML/CSS**: Front-end technologies used to create the web pages.
- **Werkzeug**: A library for securely handling passwords.

---

## **Setup Instructions**

### **1. Clone the Repository**

Clone the project to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### **2. Create a Virtual Environment (Optional but recommended)**

Create a virtual environment to isolate your project’s dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **Mac/Linux**:

  ```bash
  source venv/bin/activate
  ```

### **3. Install Dependencies**

Install the necessary Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### **4. Set Up the Database**

The database is managed by SQLAlchemy and will be automatically created when you run the app for the first time.

Run the Flask application once to set up the database:

```bash
python app.py
```

### **5. Create a Superuser Account (Admin)**

To create a superuser account (admin), you can use the `create_superuser.py` script (see the script below).

### **6. Running the Application**

To run the Flask application, simply execute:

```bash
python app.py
```

The application will start, and you can access it by visiting `http://127.0.0.1:5000/` in your web browser.

---

## **App Structure**

### **1. `app.py`**

The main application file. It defines all the routes, models, and logic for handling user actions such as registering, logging in, managing products, and handling orders.

### **2. `models.py`**

(Optional) You could separate the models into a different file for better organization. This file contains the SQLAlchemy models for `User`, `Product`, `Order`, and `OrderItem`.

### **3. `templates/`**

This directory contains all the HTML templates used for rendering pages. It includes templates for the homepage, product details, login, registration, cart, checkout, and admin dashboard.

### **4. `static/`**

This directory stores static assets like CSS files, JavaScript files, and images used in the application.

---

## **User Stories**

### **1. User Registration**

- A user can register by providing a username, email, and password.
- After successful registration, the user is redirected to the login page.

### **2. User Login**

- Registered users can log in using their username and password.
- Once logged in, the user is redirected to the homepage where they can view products and add them to their cart.

### **3. Shopping Cart**

- Users can add products to their cart.
- The cart displays the items added by the user, including the quantity and price.
- Users can remove items from the cart or proceed to checkout.

### **4. Order Placement**

- Once the user is ready, they can place an order.
- An order contains details like products, quantities, and the total price.
- After placing an order, the order is marked as "complete" and the user is redirected to an order confirmation page.

### **5. Admin Features**

- Admins can view all products, orders, and users.
- Admins can add new products and update or delete existing ones.
- Admins can view completed orders and the details of the users who placed them.

---

## **API Routes**

### **1. `/`** - **Homepage**
- Displays all products.
  
### **2. `/product/<int:product_id>`** - **Product Detail Page**
- Displays detailed information about a specific product.

### **3. `/register`** - **User Registration**
- Allows new users to register by providing a username, email, and password.

### **4. `/login`** - **User Login**
- Allows existing users to log in using their username and password.

### **5. `/logout`** - **Logout**
- Logs the user out and redirects them to the homepage.

### **6. `/cart`** - **Shopping Cart**
- Displays the current user's shopping cart.
- Allows users to add or remove products.

### **7. `/add_to_cart/<int:product_id>`** - **Add Product to Cart**
- Adds a specific product to the user's cart.

### **8. `/remove_from_cart/<int:item_id>`** - **Remove Item from Cart**
- Removes a specific product from the user's cart.

### **9. `/checkout`** - **Checkout Page**
- Allows the user to review their cart before placing an order.

### **10. `/place_order`** - **Place Order**
- Finalizes the order and marks it as complete.

### **11. `/order_confirmation/<int:order_id>`** - **Order Confirmation Page**
- Displays the details of the placed order.

### **12. `/admin`** - **Admin Dashboard**
- Admin interface to manage products, users, and orders.

### **13. `/admin/add_product`** - **Add Product (Admin)**
- Allows admins to add new products to the store.

---

## **Database Models**

### **1. `User`**
- `id`: Primary key, Integer
- `username`: Unique, String
- `email`: Unique, String
- `password_hash`: String (hashed password)
- `is_admin`: Boolean (true for admin users)

### **2. `Product`**
- `id`: Primary key, Integer
- `name`: String
- `description`: Text
- `price`: Float
- `image`: String (filename)
- `stock`: Integer (number of items available)

### **3. `Order`**
- `id`: Primary key, Integer
- `user_id`: ForeignKey to `User`
- `date_ordered`: DateTime (automatically set)
- `complete`: Boolean (true if the order is completed)

### **4. `OrderItem`**
- `id`: Primary key, Integer
- `order_id`: ForeignKey to `Order`
- `product_id`: ForeignKey to `Product`
- `quantity`: Integer (number of items)

---

## **Common Issues & Troubleshooting**

- **Database Connection Issues**: Ensure that SQLite is properly configured and the database file is located in the correct directory.
- **Admin Access Denied**: Ensure the user is assigned the `is_admin=True` flag in the database.

---

## **Future Improvements**

- Implement payment gateway integration for real-world transactions.
- Add product categories to organize products.
- Implement email notifications for order updates.

---

This documentation should give you a solid overview of your e-commerce project. Let me know if you need further clarification or additions!
