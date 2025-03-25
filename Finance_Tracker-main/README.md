# Personal Finance Tracker

A web-based personal finance tracking application built with Flask that helps users manage their expenses, visualize spending patterns, and set budget goals.

## Features

- User authentication and personal accounts
- Expense logging and categorization
- Spending visualization with interactive charts (Line and Bar charts)
- Budget goal setting and tracking
- Monthly and category-wise expense reports
- Responsive design with Bootstrap
- Visual feedback with icons and animations
- Indian Rupee (₹) currency support

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Chart.js (for visualizations)
- Bootstrap 5 (for styling)
- Bootstrap Icons

## Features in Detail

### Dashboard
- Overview of monthly expenses
- Category-wise expense distribution
- Recent transactions
- Budget tracking with progress bars

### Expense Management
- Add new expenses with categories
- View all expenses in a tabular format
- Filter and sort expenses

### Budget Management
- Set budgets for different categories
- Visual progress tracking
- Alerts for over-budget categories

### Authentication
- User registration with email
- Secure login system
- Remember me functionality

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```

5. Access the application at `http://localhost:5000`

6. Extract venv.zip as projectname/venv
## Project Structure
finance_tracker/
├── app/
│ ├── init.py # Application factory and configuration
│ ├── models.py # Database models (User, Expense, Budget)
│ ├── routes.py # Application routes and views
│ └── auth.py # Authentication routes
├── static/
│ ├── css/
│ │ └── style.css # Custom styles
│ └── js/ # JavaScript files
├── templates/
│ ├── base.html # Base template with navigation
│ ├── dashboard.html # Main dashboard with charts
│ ├── expenses.html # Expense listing page
│ ├── add_expense.html # Add expense form
│ ├── set_budget.html # Budget management
│ ├── login.html # Login page
│ └── register.html # Registration page
├── instance/
│ └── finance.db # SQLite database
├── venv/ # Virtual environment
├── requirements.txt # Project dependencies
├── run.py # Application entry point
└── README.md # Project documentation
```
