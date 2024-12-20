import sys
import hashlib
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from db_setup import engine, Session, Base
from models.portfolio import Portfolio
from models.investment import Investment
from models.transaction import Transaction
from models.company import Company
from models.user import User
# Initialize the database and tables (create them if they don't exist)
Base.metadata.create_all(engine)
def signup(session):
    print("--- Sign Up ---")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
  
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(f"Debug: Storing hashed password: {hashed_password}")  
    
    # Create the new user in the database
    user = User(username=username, password=hashed_password) 
    session.add(user)
    session.commit()
    
    print(f"User {username} created successfully!")
    company_name = input("Enter the new company's name: ")
    industry = input("Enter the company's industry: ")
    
    company = Company(name=company_name, industry=industry, user=user)  
    session.add(company)
    session.commit()
    
    print(f"Company '{company_name}' added successfully!")
    another = input("Would you like to add another company? (y/n): ")
    if another.lower() == 'y':
        signup(session)
    else:
        print("Returning to the Main Menu...")
    
    
    main_menu(session, company, user)
def login(session):
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(f"Debug: Checking against hashed password: {hashed_password}")  

    user = session.query(User).filter_by(username=username, password=hashed_password).first()

    if user:
        print(f"Welcome back, {username}!")
        return user 
    else:
        print("Invalid username or password. Please try again.")
        return None


def authentication_flow(session):
    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user = login(session)
            if user:
                return user  
        elif choice == "2":
            signup(session)
        elif choice == "3":
            print("Exiting program.")
            session.close()
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

# Functionality
def welcome_screen():
    print("\n=== Welcome to the Investment Portfolio Tracker ===")
    session = Session() 
    user = authentication_flow(session)  

    if user: 
        
        companies = session.query(Company).filter_by(user_id=user.id).all()

        if companies:
            print("\nSelect a company to manage:")
            for idx, company in enumerate(companies, start=1):
                print(f"{idx}. {company.name}")
            print(f"{len(companies) + 1}. Add New Company")
            print(f"{len(companies) + 2}. Exit")
        else:
            print("No companies found in your account.")
            print("1. Add New Company")
            print("2. Exit")

        while True:
            try:
                choice = int(input("\nEnter your choice: "))

                if 1 <= choice <= len(companies):
                    selected_company = companies[choice - 1]
                    print(f"\nYou selected {selected_company.name}!")
                    main_menu(session, selected_company, user) 
                    break
                elif choice == len(companies) + 1:
                    add_new_company(session, user)  
                    break  
                elif choice == len(companies) + 2 or choice == 2:
                    print("Exiting the program. Goodbye!")
                    session.close()  
                    sys.exit()  
                else:
                    print("Invalid input. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def main_menu(session, company, current_user):
    while True:
        print("\n=== Main Menu ===")
        print("1. Manage Portfolios")
        print("2. Manage Investments")
        print("3. Manage Transactions")
        print("4. Update Company")
        print("5. Delete Company")
        print("6. Back to Welcome Screen")
        
        choice = input("Select an option: ")

        if choice == "1":
            manage_portfolios(session, company, current_user)  
        elif choice == "2":
            manage_investments(session, company)
        elif choice == "3":
            manage_transactions(session, company)
        elif choice == "4":
            update_company(session, company)
        elif choice == "5":
            delete_company(session, company)
        elif choice == "6":
            print("\nReturning to the Welcome Screen...")
            session.close()  
            welcome_screen()  
            break 
        else:
            print("Invalid option. Please try again.")

def add_new_company(session, user=None):
    while True:
        name = input("Enter the new company's name: ")
        industry = input("Enter the company's industry: ")

        # Check if company already exists
        existing_company = session.query(Company).filter_by(name=name).first()
        if existing_company:
            print(f"Company '{name}' already exists!")
        else:
            new_company = Company(name=name, industry=industry, user_id=user.id if user else None)
            session.add(new_company)
            session.commit()
            print(f"Company '{name}' added successfully!")

        # Ask if they want to add another company or go back to the main menu
        choice = input("\nWould you like to add another company? (y/n): ").lower()
        if choice == 'y':
            continue 
        elif choice == 'n':
            print("Returning to the Main Menu...\n")
            return new_company  
        else:
            print("Invalid choice, please enter 'y' or 'n'.")


def update_company(session, company):
    print(f"\nYou are about to update the company: {company.name}")
    new_name = input("Enter the new name for the company (or press Enter to keep current name): ")
    
    if new_name.strip():
        company.name = new_name
        try:
            session.commit()
            print(f"Company name updated to {company.name}!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating company: {e}")
    else:
        print("No changes made.")

def delete_company(session, company):
    confirm = input(f"Are you sure you want to delete the company '{company.name}' and its related portfolios, investments, and transactions? (y/n): ")
    if confirm.lower() == 'y':
        try:
            session.delete(company)
            session.commit()
            print(f"Company '{company.name}' and all its related data deleted successfully!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting company: {e}")
    else:
        print("Company deletion canceled.")


def manage_portfolios(session, company, current_user):
    while True:
        print("\n--- Manage Portfolios ---")
        print("1. Create Portfolio")
        print("2. View All Portfolios")
        print("3. Update Portfolio")
        print("4. Delete Portfolio")
        print("5. Back")
        
        choice = input("Select an option: ")

        if choice == "1":
            create_portfolio(session, company, current_user)  
        elif choice == "2":
            view_portfolios(session, company, current_user) 
        elif choice == "3":
            update_portfolio(session, company, current_user)  
        elif choice == "4":
            delete_portfolio(session, company, current_user)  
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")


def manage_investments(session, company):
    while True:
        print("\n--- Manage Investments ---")
        print("1. Add Investment")
        print("2. View Investments")
        print("3. Update Investment")
        print("4. Delete Investment")
        print("5. Back")
        
        choice = input("Select an option: ")

        if choice == "1":
            create_investment(session, company)
        elif choice == "2":
            view_investments(session, company)
        elif choice == "3":
            update_investment(session, company)
        elif choice == "4":
            delete_investment(session, company)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")

def manage_transactions(session, company):
    while True:
        print("\n--- Manage Transactions ---")
        print("1. Create Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Back")
        choice = input("Select an option: ")

        if choice == "1":
            create_transaction(session, company)
        elif choice == "2":
            view_transactions(session, company)
        elif choice == "3":
            update_transaction(session, company)
        elif choice == "4":
            delete_transaction(session, company)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")
def create_portfolio(session, company, current_user):
    name = input("Portfolio Name: ")
    description = input("Description: ")
    
    while True:
        try:
            budget = float(input("Budget: "))
            break  
        except ValueError:
            print("Invalid input. Please enter a numeric value for budget.")
    
    
    portfolio = Portfolio(
        name=name, 
        description=description, 
        budget=budget, 
        company=company,
        user_id=current_user.id  
    )
    
    session.add(portfolio)
    session.commit()
    print("Portfolio created successfully!")
def view_portfolios(session, company, current_user):
    portfolios = session.query(Portfolio).filter_by(company_id=company.id, user_id=current_user.id).all()
    if portfolios:
        for p in portfolios:
            print(f"ID: {p.id}, Name: {p.name}, Budget: {p.budget}, Description: {p.description}")
    else:
        print("No portfolios available for this company.")
def update_portfolio(session, company, current_user): 
    view_portfolios(session, company, current_user)  
    while True:
        try:
            portfolio_id = int(input("Enter Portfolio ID to update: "))
            portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=current_user.id).first()  
            if portfolio:
                print(f"Current Name: {portfolio.name}")
                portfolio.name = input("New Name (leave blank to keep current): ") or portfolio.name
                print(f"Current Description: {portfolio.description}")
                portfolio.description = input("New Description (leave blank to keep current): ") or portfolio.description
                print(f"Current Budget: {portfolio.budget}")
                while True:
                    try:
                        new_budget = input("New Budget (leave blank to keep current): ") or portfolio.budget
                        portfolio.budget = float(new_budget)
                        break
                    except ValueError:
                        print("Please enter a valid numeric value for budget.")
                session.commit()
                print("Portfolio updated successfully!")
                break
            else:
                print("Portfolio not found or not associated with the logged-in user. Please try again.")
                break
        except ValueError:
            print("Invalid ID. Please enter a valid Portfolio ID.")
def delete_portfolio(session, company, current_user):
    view_portfolios(session, company, current_user)  
    try:
        portfolio_id = int(input("Enter Portfolio ID to delete: "))
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, company_id=company.id).first()

        if portfolio:
            
            for investment in portfolio.investments:
                session.delete(investment)
            for transaction in portfolio.transactions:
                session.delete(transaction)

            session.delete(portfolio)
            session.commit()
            print(f"Portfolio '{portfolio.name}' and its related investments and transactions deleted successfully!")
        else:
            print(f"Portfolio with ID {portfolio_id} not found for company '{company.name}'.")
    except ValueError:
        print("Invalid ID. Please enter a valid Portfolio ID.")
# Investment CRUD operations (Create, View, Update, Delete)
def create_investment(session, company):
    try:
        company = session.query(Company).filter_by(id=company.id).one()
    except NoResultFound:
        print("Company not found. Exiting.")
        return

    
    portfolios = session.query(Portfolio).filter_by(company_id=company.id).all()

    if not portfolios:
        print(f"No portfolios found for company '{company.name}'. Please create a portfolio first.")
        return

    print("\nSelect a portfolio for this investment:")
    for idx, portfolio in enumerate(portfolios, start=1):
        print(f"{idx}. {portfolio.name}")
    
    while True:
        try:
            portfolio_choice = int(input("Enter the portfolio number: "))
            selected_portfolio = portfolios[portfolio_choice - 1]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please choose a valid portfolio.")
    investment_name = input("Enter Investment Name: ").strip()
    if not investment_name:
        print("Investment name is required. Exiting.")
        return

    investment_type = input("Enter Investment Type: ").strip()
    while True:
        try:
            value = float(input("Enter Investment Value: "))
            break
        except ValueError:
            print("Invalid input for value. Please enter a numeric value.")
    
    risk_level = input("Enter Risk Level: ").strip()
    while True:
        try:
            expected_return = float(input("Enter Expected Return: "))
            break
        except ValueError:
            print("Invalid input for expected return. Please enter a numeric value.")

    date_invested = input("Enter Date of Investment (YYYY-MM-DD): ").strip()
    try:
        date_invested = datetime.strptime(date_invested, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Investment not created.")
        return
    investment = Investment(
        name=investment_name,
        investment_type=investment_type,
        value=value,
        risk_level=risk_level,
        expected_return=expected_return,
        date_invested=date_invested,
        company_id=company.id,
        portfolio_id=selected_portfolio.id
    )

    session.add(investment)
    session.commit()
    print(f"Investment '{investment.name}' added successfully to portfolio '{selected_portfolio.name}'!")
def view_investments(session, company):
    investments = session.query(Investment).filter_by(company_id=company.id).all()

    if investments:
        print("\n=== Investments ===")
        for investment in investments:
            portfolio = session.query(Portfolio).filter_by(id=investment.portfolio_id).first()
            portfolio_name = portfolio.name if portfolio else "Unknown"
            print(
                f"ID: {investment.id}, Name: {investment.name}, Value: {investment.value}, "
                f"Portfolio: {portfolio_name}, Investment Type: {investment.investment_type}, "
                f"Risk Level: {investment.risk_level}, Expected Return: {investment.expected_return}, "
                f"Date Invested: {investment.date_invested.strftime('%Y-%m-%d')}"
            )
    else:
        print(f"No investments found for company '{company.name}'.")
def update_investment(session, company):
    view_investments(session, company)  

    try:
        investment_id = int(input("Enter Investment ID to update: "))
        investment = session.query(Investment).filter_by(id=investment_id, company_id=company.id).first()

        if investment:
            print(f"\nInvestment found: {investment.name}, {investment.value}, {investment.risk_level}, {investment.expected_return}, {investment.date_invested.strftime('%Y-%m-%d')}")

            
            new_name = input(f"Current Name: {investment.name}. New Name (leave blank to keep current): ").strip()
            if new_name:
                investment.name = new_name

           
            new_investment_type = input(f"Current Investment Type: {investment.investment_type}. New Investment Type (leave blank to keep current): ").strip()
            if new_investment_type:
                investment.investment_type = new_investment_type

           
            while True:
                new_value = input(f"Current Value: {investment.value}. New Value (leave blank to keep current): ").strip()
                if not new_value:
                    break  
                try:
                    investment.value = float(new_value)
                    break
                except ValueError:
                    print("Invalid value. Please enter a numeric value.")

            
            new_risk_level = input(f"Current Risk Level: {investment.risk_level}. New Risk Level (leave blank to keep current): ").strip()
            if new_risk_level:
                investment.risk_level = new_risk_level

           
            while True:
                new_expected_return = input(f"Current Expected Return: {investment.expected_return}. New Expected Return (leave blank to keep current): ").strip()
                if not new_expected_return:
                    break  
                try:
                    investment.expected_return = float(new_expected_return)
                    break
                except ValueError:
                    print("Invalid expected return. Please enter a numeric value.")

            
            new_date_invested = input(f"Current Date Invested: {investment.date_invested.strftime('%Y-%m-%d')}. New Date (YYYY-MM-DD, leave blank to keep current): ").strip()
            if new_date_invested:
                try:
                    parsed_date = datetime.strptime(new_date_invested, "%Y-%m-%d")
                    investment.date_invested = parsed_date
                except ValueError:
                    print("Invalid date format. Keeping current date.")

            
            session.commit()
            print("\nInvestment updated successfully!")
            print(f"Updated Investment: {investment}")
        else:
            print(f"Investment with ID {investment_id} not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Investment ID.")

def delete_investment(session, company):
    view_investments(session, company) 

    try:
        investment_id = int(input("Enter Investment ID to delete: "))
        investment = session.query(Investment).filter_by(id=investment_id, company_id=company.id).first()

        if investment:
            session.delete(investment)
            session.commit()
            print(f"Investment '{investment.name}' deleted successfully!")
        else:
            print(f"Investment with ID {investment_id} not found for company '{company.name}'.")
    except ValueError:
        print("Invalid ID. Please enter a valid Investment ID.")
def create_transaction(session, company):
    try:
       
        company = session.query(Company).filter_by(name=company.name).one() 
    except NoResultFound:
        print(f"Company '{company.name}' not found.")
        return
    investment_id = int(input("Enter Investment ID to add transaction: "))
    while True:
        try:
            amount = float(input("Transaction Amount: "))
            break
        except ValueError:
            print("Invalid input for amount. Please enter a valid numeric value.")
    
    transaction_type = input("Transaction Type (buy/sell): ").lower()
    if transaction_type not in ['buy', 'sell']:
        print("Invalid transaction type. Please enter 'buy' or 'sell'.")
        return
    date_str = input("Transaction Date (YYYY-MM-DD): ") or datetime.today().strftime('%Y-%m-%d')
    try:
        transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Defaulting to today's date.")
        transaction_date = datetime.today()

    portfolio_id = int(input("Enter Portfolio ID: "))
    notes = input("Enter any notes for the transaction: ")
    transaction = Transaction(
        investment_id=investment_id, 
        amount=amount, 
        type=transaction_type, 
        date=transaction_date,
        portfolio_id=portfolio_id,  
        notes=notes,
        company_id=company.id  
    )
    
    session.add(transaction)
    session.commit()
    print("Transaction added successfully!")

def view_transactions(session, company):
    
    transactions = session.query(Transaction).join(Investment).filter(Investment.company_id == company.id).all()
    if transactions:
        print("\n--- Transactions ---")
        for t in transactions:
            print(f"ID: {t.id}, Investment ID: {t.investment_id}, Amount: {t.amount}, Type: {t.type}, "
                  f"Date: {t.date.strftime('%Y-%m-%d')}, Portfolio ID: {t.portfolio_id}, Notes: {t.notes}")
    else:
        print("No transactions found for this company.")
def update_transaction(session, company):
    
    try:
        transaction_id = int(input("Enter Transaction ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a valid integer.")
        return
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        print(f"Transaction with ID {transaction_id} not found!")
        return
    print(f"Current transaction details: {transaction}")
    transaction_type = input(f"Enter new transaction type (current: {transaction.type}): ") or transaction.type
    amount = input(f"Enter new amount (current: {transaction.amount}): ") or str(transaction.amount)
    date = input(f"Enter new transaction date (current: {transaction.date}): ") or str(transaction.date)
    portfolio_id = input(f"Enter new Portfolio ID (current: {transaction.portfolio_id}): ") or str(transaction.portfolio_id)
    notes = input(f"Enter new notes (current: {transaction.notes}): ") or transaction.notes
    try:
        if transaction_type not in ['buy', 'sell']:
            print("Invalid transaction type!")
            return
        transaction.type = transaction_type
        transaction.amount = float(amount)
        transaction.date = datetime.strptime(date, "%Y-%m-%d")
        transaction.portfolio_id = int(portfolio_id)
        transaction.notes = notes
        session.commit()
        print("Transaction updated successfully!")
    
    except ValueError as e:
        print(f"Error: {e}")
def delete_transaction(session, company):
    view_transactions(session, company)  
    
    try:
        transaction_id = int(input("Enter Transaction ID to delete: "))
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()

        if transaction:
            confirm = input(f"Are you sure you want to delete Transaction ID {transaction_id}? (yes/no): ").lower()
            if confirm == 'yes':
                session.delete(transaction)
                session.commit()
                print("Transaction deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Transaction with ID {transaction_id} not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Transaction ID.")
if __name__ == "__main__":
    welcome_screen()