from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Expense, Budget
from app.forms import LoginForm, RegistrationForm, ExpenseForm, BudgetForm
from app import db
from datetime import datetime
from sqlalchemy import extract, func

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    # Get monthly total expenses
    monthly_expenses = db.session.query(
        func.sum(Expense.amount).label('total'),
        func.strftime('%Y-%m', Expense.date).label('month')
    ).filter_by(user_id=current_user.id).group_by('month').all()

    # Get category-wise expenses
    category_expenses = db.session.query(
        func.sum(Expense.amount).label('total'),
        Expense.category
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()

    # Get recent expenses
    recent_expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc()).limit(5).all()

    # Get budget progress
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html',
                         monthly_expenses=monthly_expenses,
                         category_expenses=category_expenses,
                         recent_expenses=recent_expenses,
                         budgets=budgets)

@main.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        date = request.form.get('date')
        description = request.form.get('description')

        if not category or not amount or not date:
            flash('Please fill in all required fields', 'danger')
            return redirect(url_for('main.add_expense'))

        try:
            amount = float(amount)
            date = datetime.strptime(date, '%Y-%m-%d')
            
            new_expense = Expense(
                category=category,
                amount=amount,
                date=date,
                description=description,
                user_id=current_user.id
            )
            
            db.session.add(new_expense)
            db.session.commit()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except ValueError:
            flash('Invalid amount or date format', 'danger')
            return redirect(url_for('main.add_expense'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the expense', 'danger')
            return redirect(url_for('main.add_expense'))

    return render_template('add_expense.html')

@main.route('/set-budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    try:
        # Get existing budgets for the current user
        budgets = Budget.query.filter_by(user_id=current_user.id).all()
        
        if request.method == 'POST':
            category = request.form.get('category')
            amount = request.form.get('amount')
            
            # Debug print to see what values we're getting
            print(f"Received: category={category}, amount={amount}, user_id={current_user.id}")
            
            if not category or not amount:
                flash('Please fill in all fields', 'danger')
                return render_template('set_budget.html', budgets=budgets)
            
            try:
                # Convert amount to float and validate it
                amount = float(amount)
                if amount <= 0:
                    flash('Amount must be greater than 0', 'danger')
                    return render_template('set_budget.html', budgets=budgets)
                
                # Check for existing budget in this category
                existing_budget = Budget.query.filter_by(
                    user_id=current_user.id,
                    category=category
                ).first()
                
                if existing_budget:
                    # Update existing budget
                    existing_budget.amount = amount
                    db.session.commit()
                    flash('Budget updated successfully!', 'success')
                else:
                    # Create new budget
                    new_budget = Budget(
                        category=category,
                        amount=amount,
                        user_id=current_user.id
                    )
                    db.session.add(new_budget)
                    try:
                        db.session.commit()
                        flash('Budget set successfully!', 'success')
                    except Exception as commit_error:
                        print(f"Commit error: {str(commit_error)}")
                        db.session.rollback()
                        raise
                
                return redirect(url_for('main.dashboard'))
                
            except ValueError as ve:
                print(f"ValueError: {str(ve)}")
                flash('Invalid amount format', 'danger')
                return render_template('set_budget.html', budgets=budgets)
            except Exception as e:
                print(f"Inner exception: {str(e)}")
                db.session.rollback()
                flash('An error occurred while processing the budget. Please try again.', 'danger')
                return render_template('set_budget.html', budgets=budgets)
                
    except Exception as outer_e:
        print(f"Outer exception: {str(outer_e)}")
        db.session.rollback()
        flash('An error occurred while accessing the budget system. Please try again.', 'danger')
        return render_template('set_budget.html', budgets=[])

    return render_template('set_budget.html', budgets=budgets)

@main.route('/expenses')
@login_required
def view_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc()).all()
    return render_template('expenses.html', expenses=expenses)

@main.route('/api/expenses_data')
@login_required
def expenses_data():
    monthly_expenses = db.session.query(
        func.sum(Expense.amount).label('total'),
        func.strftime('%Y-%m', Expense.date).label('month')
    ).filter_by(user_id=current_user.id).group_by('month').all()
    
    return jsonify({
        'labels': [item[1] for item in monthly_expenses],
        'data': [float(item[0]) for item in monthly_expenses]
    }) 