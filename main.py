from db_setup import engine, Session, Base
from models.portfolio import Portfolio
from models.investment import Investment
from models.transaction import Transaction

# Initialize the database and tables
Base.metadata.create_all(engine)

# Functionality
def welcome_screen():
    print("\n=== Welcome to the Investment Portfolio Tracker ===")
    print("Choose a company to manage:")
    companies = ["TechCorp", "HealthPlus", "GreenEnergy", "FinSolutions"]
    for idx, company in enumerate(companies, start=1):
        print(f"{idx}. {company}")
    print("5. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 4:
                print(f"\nYou selected {companies[choice - 1]}!")
                main_menu()
                break
            elif choice == 5:
                print("Exiting the program. Goodbye!")
                exit()
            else:
                print("Invalid input. Please choose a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main_menu():
    session = Session()
    while True:
        print("\n=== Main Menu ===")
        print("1. Manage Portfolios")
        print("2. Manage Investments")
        print("3. Manage Transactions")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            manage_portfolios(session)
        elif choice == "2":
            manage_investments(session)
        elif choice == "3":
            manage_transactions(session)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

def manage_portfolios(session):
    while True:
        print("\n--- Manage Portfolios ---")
        print("1. Create Portfolio")
        print("2. View All Portfolios")
        print("3. Update Portfolio")
        print("4. Delete Portfolio")
        print("5. Back")
        choice = input("Select an option: ")

        if choice == "1":
            create_portfolio(session)
        elif choice == "2":
            view_portfolios(session)
        elif choice == "3":
            update_portfolio(session)
        elif choice == "4":
            delete_portfolio(session)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")

def manage_investments(session):
    while True:
        print("\n--- Manage Investments ---")
        print("1. Add Investment")
        print("2. View Investments")
        print("3. Update Investment")
        print("4. Back")
        choice = input("Select an option: ")

        if choice == "1":
            create_investment(session)
        elif choice == "2":
            view_investments(session)
        elif choice == "3":
            update_investment(session)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")

def manage_transactions(session):
    print("\n--- Manage Transactions ---")
    print("This section is under construction. Stay tuned!")

def create_portfolio(session):
    name = input("Portfolio Name: ")
    description = input("Description: ")
    budget = float(input("Budget: "))
    portfolio = Portfolio(name=name, description=description, budget=budget)
    session.add(portfolio)
    session.commit()
    print("Portfolio created successfully!")

def view_portfolios(session):
    portfolios = session.query(Portfolio).all()
    if portfolios:
        for p in portfolios:
            print(p)
    else:
        print("No portfolios available.")

def update_portfolio(session):
    view_portfolios(session)
    try:
        portfolio_id = int(input("Enter Portfolio ID to update: "))
        portfolio = session.get(Portfolio, portfolio_id)
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

def delete_portfolio(session):
    view_portfolios(session)
    try:
        portfolio_id = int(input("Enter Portfolio ID to delete: "))
        portfolio = session.get(Portfolio, portfolio_id)
        if portfolio:
            session.delete(portfolio)
            session.commit()
            print("Portfolio deleted successfully!")
        else:
            print("Portfolio not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Portfolio ID.")

def create_investment(session):
    view_portfolios(session)
    try:
        portfolio_id = int(input("Enter Portfolio ID to add investment: "))
        portfolio = session.get(Portfolio, portfolio_id)
        if portfolio:
            name = input("Investment Name: ")
            value = float(input("Investment Value: "))
            investment = Investment(name=name, value=value, portfolio=portfolio)
            session.add(investment)
            session.commit()
            print("Investment added successfully!")
        else:
            print("Portfolio not found.")
    except ValueError:
        print("Invalid Portfolio ID. Please enter a valid ID.")

def view_investments(session):
    investments = session.query(Investment).all()
    if investments:
        for i in investments:
            print(i)
    else:
        print("No investments available.")

def update_investment(session):
    view_investments(session)
    try:
        investment_id = int(input("Enter Investment ID to update: "))
        investment = session.get(Investment, investment_id)
        if investment:
            print(f"Current Name: {investment.name}")
            investment.name = input("New Name (leave blank to keep current): ") or investment.name
            print(f"Current Value: {investment.value}")
            investment.value = float(input("New Value (leave blank to keep current): ") or investment.value)
            session.commit()
            print("Investment updated successfully!")
        else:
            print("Investment not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid Investment ID.")

if __name__ == "__main__":
    welcome_screen()
