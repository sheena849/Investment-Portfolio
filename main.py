import sys
from db_setup import engine, Session, Base
from models.portfolio import Portfolio
from models.investment import Investment
from models.transaction import Transaction
from models.company import Company
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound


# Initialize the database and tables (create them if they don't exist)
Base.metadata.create_all(engine)

# Functionality
def welcome_screen():
    print("\n=== Welcome to the Investment Portfolio Tracker ===")
    
    session = Session()  # Start a new session
    
    companies = session.query(Company).all()

    if companies:
        print("\nSelect a company to manage:")
        for idx, company in enumerate(companies, start=1):
            print(f"{idx}. {company.name}")
        print(f"{len(companies) + 1}. Add New Company")
        print(f"{len(companies) + 2}. Exit")
    else:
        print("No companies found in the database.")
        print("1. Add New Company")
        print("2. Exit")
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            
            if 1 <= choice <= len(companies):
                selected_company = companies[choice - 1]
                print(f"\nYou selected {selected_company.name}!")
                main_menu(session, selected_company)  # Call main_menu for selected company
                break
            elif choice == len(companies) + 1:
                add_new_company(session)  # Call add_new_company() and return control to the main menu
                break  # Return to the main screen to refresh company list
            elif choice == len(companies) + 2 or choice == 2:
                print("Exiting the program. Goodbye!")
                session.close()  # Properly close the session
                sys.exit()  # Exit gracefully
            else:
                print("Invalid input. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main_menu(session, company):
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
            manage_portfolios(session, company)
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
            session.close()  # Close the session before going back
            welcome_screen()  # This will call the welcome screen again
            break  # Break the loop in main_menu to ensure it returns
        else:
            print("Invalid option. Please try again.")

def add_new_company(session):
    name = input("Enter the new company's name: ")
    industry = input("Enter the company's industry: ")

    # Check if company already exists
    existing_company = session.query(Company).filter_by(name=name).first()
    if existing_company:
        print(f"Company '{name}' already exists!")
    else:
        new_company = Company(name=name, industry=industry)
        session.add(new_company)
        session.commit()
        print(f"Company '{name}' added successfully!")
    
    # After adding a new company, return to the main menu
    print("\nReturning to the Main Menu...")
    session.close()  # Properly close the session before going back to the main menu
    welcome_screen() 
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
    confirm = input(f"Are you sure you want to delete the company '{company.name}'? (y/n): ")
    if confirm.lower() == 'y':
        try:
            # Delete associated portfolios first
            for portfolio in company.portfolios:
                session.delete(portfolio)

            # Now delete the company
            session.delete(company)
            session.commit()
            print(f"Company '{company.name}' and all its portfolios deleted successfully!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting company: {e}")
    else:
        print("Company deletion canceled.")


def manage_portfolios(session, company):
    while True:
        print("\n--- Manage Portfolios ---")
        print("1. Create Portfolio")
        print("2. View All Portfolios")
        print("3. Update Portfolio")
        print("4. Delete Portfolio")
        print("5. Back")
        choice = input("Select an option: ")

        if choice == "1":
            create_portfolio(session, company)
        elif choice == "2":
            view_portfolios(session, company)
        elif choice == "3":
            update_portfolio(session, company)
        elif choice == "4":
            delete_portfolio(session, company)
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
        print("4. Delete Investment")  # Ensure the Delete option is present
        print("5. Back")
        
        choice = input("Select an option: ")

        if choice == "1":
            create_investment(session, company)
        elif choice == "2":
            view_investments(session, company)
        elif choice == "3":
            update_investment(session, company)
        elif choice == "4":
            delete_investment(session, company)  # This calls the delete_investment function
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

def create_portfolio(session, company):
    name = input("Portfolio Name: ")
    description = input("Description: ")
    budget = float(input("Budget: "))

    # Create the Portfolio and associate it with the company
    portfolio = Portfolio(name=name, description=description, budget=budget, company=company)
    session.add(portfolio)
    session.commit()
    print("Portfolio created successfully!")

def view_portfolios(session, company):
    portfolios = session.query(Portfolio).filter_by(company_id=company.id).all()
    if portfolios:
        for p in portfolios:
            print(p)
    else:
        print("No portfolios available for this company.")

def update_portfolio(session, company):
    view_portfolios(session, company)
    try:
        portfolio_id = int(input("Enter Portfolio ID to update: "))
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if portfolio:
            print(f"Current Name: {portfolio.name}")
            portfolio.name = input("New Name (leave blank to keep current): ") or portfolio.name
            print(f"Current Description: {portfolio.description}")
            portfolio.description = input("New Description (leave blank to keep current): ") or portfolio.description
            print(f"Current Budget: {portfolio.budget}")
            portfolio.budget = float(input("New Budget (leave blank to keep current): ") or portfolio.budget)
            session.commit()
            print("Portfolio updated successfully!")
        else:
            print("Portfolio not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Portfolio ID.")

def delete_portfolio(session, company):
    view_portfolios(session, company)
    try:
        portfolio_id = int(input("Enter Portfolio ID to delete: "))
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if portfolio:
            session.delete(portfolio)
            session.commit()
            print("Portfolio deleted successfully!")
        else:
            print("Portfolio not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Portfolio ID.")

# Create Investment
def create_investment(session, company):
    try:
        # Query the company by its name to get the company object
        company = session.query(Company).filter_by(name=company.name).one()  # Fetch the company object

    except NoResultFound:
        print(f"Company '{company.name}' not found.")
        return

    # Gather the details for the investment
    portfolio_id = int(input("Enter Portfolio ID to add investment: "))
    name = input("Investment Name: ")
    value = float(input("Investment Value: "))
    
    # Ask for the investment type; if it's not provided, set it to a default value
    investment_type = input("Investment Type: ") or 'Default Type'
    
    # Other fields, such as risk level, expected return, and date invested
    risk_level = input("Risk Level: ") or 'Moderate'
    expected_return = input("Expected Return: ") or '5%'
    
    # Ensure that date_invested is converted to a date object
    date_invested_str = input("Date Invested (YYYY-MM-DD): ") or '2024-12-18'
    try:
        date_invested = datetime.strptime(date_invested_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Defaulting to today's date.")
        date_invested = datetime.today()

    # Create and add the investment
    investment = Investment(
        name=name, 
        value=value, 
        portfolio_id=portfolio_id, 
        company_id=company.id,  # Link to the company using the company_id (not company_name)
        investment_type=investment_type, 
        risk_level=risk_level,
        expected_return=expected_return, 
        date_invested=date_invested
    )
    session.add(investment)
    session.commit()
    print("Investment added successfully!")

# View Investments
def view_investments(session, company):
    investments = session.query(Investment).filter_by(company_id=company.id).all()

    if investments:
        print("\n=== Investments ===")
        for investment in investments:
            print(f"ID: {investment.id}, Name: {investment.name}, Value: {investment.value}, Investment Type: {investment.investment_type}")
    else:
        print("No investments found.")

# Update Investment
def update_investment(session, company):
    view_investments(session, company)  # Display current investments

    try:
        # Step 1: Input the ID of the investment you want to update
        investment_id = int(input("Enter Investment ID to update: "))
        investment = session.query(Investment).filter_by(id=investment_id).first()

        # Step 2: Check if the investment exists
        if investment:
            print(f"Investment found: {investment.name}, {investment.value}, {investment.risk_level}, {investment.expected_return}, {investment.date_invested}")

            # Step 3: Ask for new values for each field
            # Name
            new_name = input(f"Current Name: {investment.name}. New Name (leave blank to keep current): ") or investment.name
            if new_name != investment.name:
                investment.name = new_name

            # Value
            new_value = input(f"Current Value: {investment.value}. New Value (leave blank to keep current): ") or str(investment.value)
            if new_value != str(investment.value):
                try:
                    investment.value = float(new_value)
                except ValueError:
                    print("Invalid value entered. Keeping the current value.")

            # Risk Level
            new_risk_level = input(f"Current Risk Level: {investment.risk_level}. New Risk Level (leave blank to keep current): ") or investment.risk_level
            if new_risk_level != investment.risk_level:
                investment.risk_level = new_risk_level

            # Expected Return
            new_expected_return = input(f"Current Expected Return: {investment.expected_return}. New Expected Return (leave blank to keep current): ") or investment.expected_return
            if new_expected_return != investment.expected_return:
                investment.expected_return = new_expected_return

            # Date Invested
            new_date_invested = input(f"Current Date Invested: {investment.date_invested.strftime('%Y-%m-%d')}. New Date Invested (leave blank to keep current): ") or None
            if new_date_invested:
                try:
                    investment.date_invested = datetime.strptime(new_date_invested, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Keeping current date.")

            # Step 4: Commit changes to the session
            session.commit()
            print("Investment updated successfully!")
        else:
            print(f"Investment with ID {investment_id} not found.")
    
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid Investment ID.")

# Delete Investment
def delete_investment(session, company):
    view_investments(session, company)  # Display investments before deletion

    try:
        investment_id = int(input("Enter Investment ID to delete: "))
        investment = session.query(Investment).filter_by(id=investment_id, company_id=company.id).first()  # Ensure the investment belongs to the selected company

        if investment:
            session.delete(investment)
            session.commit()
            print("Investment deleted successfully!")
        else:
            print("Investment not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Investment ID.")


def create_transaction(session, company):
    try:
        # Query the company by its name to get the company object
        company = session.query(Company).filter_by(name=company.name).one()  # Fetch the company object
    except NoResultFound:
        print(f"Company '{company.name}' not found.")
        return

    # Gather the details for the transaction
    investment_id = int(input("Enter Investment ID to add transaction: "))
    amount = float(input("Transaction Amount: "))
    
    # Other fields, such as date, transaction type, portfolio_id, and notes
    transaction_type = input("Transaction Type (buy/sell): ").lower()
    if transaction_type not in ['buy', 'sell']:
        print("Invalid transaction type. Please enter 'buy' or 'sell'.")
        return

    date_str = input("Transaction Date (YYYY-MM-DD): ") or '2024-12-18'
    try:
        transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Defaulting to today's date.")
        transaction_date = datetime.today()

    # New fields for portfolio_id and notes
    portfolio_id = int(input("Enter Portfolio ID: "))
    notes = input("Enter any notes for the transaction: ")

    # Create and add the transaction
    transaction = Transaction(
        investment_id=investment_id, 
        amount=amount, 
        type=transaction_type, 
        date=transaction_date,
        portfolio_id=portfolio_id,  # New field
        notes=notes  # New field
    )
    session.add(transaction)
    session.commit()
    print("Transaction added successfully!")

def view_transactions(session, company):
    # Fetch all transactions related to the company by joining with the Investment table
    transactions = session.query(Transaction).join(Investment).filter(Investment.company_id == company.id).all()

    if transactions:
        print("\n--- Transactions ---")
        for t in transactions:
            print(f"ID: {t.id}, Investment ID: {t.investment_id}, Amount: {t.amount}, Type: {t.type}, Date: {t.date}, Portfolio ID: {t.portfolio_id}, Notes: {t.notes}")
    else:
        print("No transactions found for this company.")


def update_transaction(session, company):
    # Ask the user for the transaction ID to update
    try:
        transaction_id = int(input("Enter Transaction ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a valid integer.")
        return

    # Fetch the transaction by ID
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()

    if not transaction:
        print(f"Transaction with ID {transaction_id} not found!")
        return

    # Provide current details
    print(f"Current transaction details: {transaction}")
    
    # Ask for new values, including portfolio_id and notes
    transaction_type = input(f"Enter new transaction type (current: {transaction.type}): ") or transaction.type
    amount = input(f"Enter new amount (current: {transaction.amount}): ") or transaction.amount
    date = input(f"Enter new transaction date (current: {transaction.date}): ") or str(transaction.date)
    portfolio_id = input(f"Enter new Portfolio ID (current: {transaction.portfolio_id}): ") or transaction.portfolio_id
    notes = input(f"Enter new notes (current: {transaction.notes}): ") or transaction.notes

    # Validate and update the transaction
    try:
        if transaction_type not in ['buy', 'sell']:
            print("Invalid transaction type!")
            return
        
        # Update the fields
        transaction.type = transaction_type
        transaction.amount = float(amount)
        transaction.date = datetime.strptime(date, "%Y-%m-%d")
        transaction.portfolio_id = int(portfolio_id)
        transaction.notes = notes

        # Commit the changes to the database
        session.commit()
        print("Transaction updated successfully!")
    
    except ValueError as e:
        print(f"Error: {e}")

def delete_transaction(session, company):
    view_transactions(session, company)
    
    try:
        transaction_id = int(input("Enter Transaction ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a valid integer.")
        return

    # Fetch the transaction by ID
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()

    if transaction:
        session.delete(transaction)
        session.commit()
        print("Transaction deleted successfully!")
    else:
        print("Transaction not found.")

if __name__ == "__main__":
    welcome_screen()
