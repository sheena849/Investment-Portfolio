
# Investment Portfolio Tracker

This project is an investment portfolio management system built with Python and SQLAlchemy. It provides a Command Line Interface (CLI) for managing portfolios, investments, and transactions within a company. The system allows users to create, view, update, and delete portfolios, investments, and transactions, as well as manage their financial data in a structured and organized manner.

## Features

- **Manage Portfolios**:
  - Create new portfolios
  - View all portfolios associated with the logged-in user
  - Update existing portfolios (name, description, budget)
  - Delete portfolios (with cascading deletions for associated investments and transactions)
  
- **Manage Investments**:
  - Add new investments to portfolios
  - View all investments for a given company
  - Update investment details (name, value, risk level, expected return, date invested)
  - Delete investments
  
- **Manage Transactions**:
  - Create transactions (buy/sell) for investments
  - View all transactions for a company
  - Update transaction details (amount, type, date, portfolio, and notes)
  - Delete transactions
  
## Installation

To run this project, you need to have Python 3.7 or higher installed on your machine. Additionally, you will need to set up a virtual environment and install the dependencies using `pipenv`.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/investment-portfolio-tracker.git
cd investment-portfolio-tracker
```

### Step 2: Install Dependencies
Make sure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed. Then, install the required dependencies by running:

```bash
pipenv install
```

### Step 3: Set Up the Database
Run the `db_setup.py` script to initialize the database and create the required tables:

```bash
pipenv run python db_setup.py
```

### Step 4: Run the Application
To start the application, run the `main.py` script:

```bash
pipenv run python main.py
```

## Usage

After starting the application, you'll be presented with a welcome screen where you can:

- **Login**: Authenticate with your username and password.
- **View and manage portfolios**: Create, view, update, and delete portfolios.
- **View and manage investments**: Create, view, update, and delete investments.
- **View and manage transactions**: Create, view, update, and delete transactions.

### CLI Commands:

The main menu will allow you to navigate through the following options:

1. **Manage Portfolios**: Allows the creation, viewing, updating, and deletion of portfolios.
2. **Manage Investments**: Allows adding, viewing, updating, and deleting investments.
3. **Manage Transactions**: Allows creating, viewing, updating, and deleting transactions.
4. **Exit**: Exits the application.

### Example Usage:

1. **Manage Portfolios**:
    - Create a new portfolio:
      ```
      1. Create Portfolio
      ```
    - View all portfolios:
      ```
      2. View All Portfolios
      ```

2. **Manage Investments**:
    - Add an investment:
      ```
      1. Add Investment
      ```

3. **Manage Transactions**:
    - Create a transaction:
      ```
      1. Create Transaction
      ```

## Models

The system uses the following models to manage data:

- **Portfolio**:
  - `id`: Primary key
  - `name`: Name of the portfolio
  - `description`: Description of the portfolio
  - `budget`: Budget allocated for the portfolio
  - `user_id`: Foreign key linking to the user owning the portfolio
  - `company_id`: Foreign key linking to the company associated with the portfolio

- **Investment**:
  - `id`: Primary key
  - `name`: Name of the investment
  - `investment_type`: Type of the investment (e.g., Stock, Bond)
  - `value`: Value of the investment
  - `risk_level`: Risk level of the investment
  - `expected_return`: Expected return from the investment
  - `date_invested`: Date the investment was made
  - `portfolio_id`: Foreign key linking to the portfolio
  - `company_id`: Foreign key linking to the company

- **Transaction**:
  - `id`: Primary key
  - `amount`: Transaction amount (positive for buying, negative for selling)
  - `type`: Type of transaction (buy/sell)
  - `date`: Date the transaction took place
  - `portfolio_id`: Foreign key linking to the portfolio
  - `investment_id`: Foreign key linking to the investment
  - `notes`: Optional notes for the transaction
  - `company_id`: Foreign key linking to the company

## Database Schema

The database uses SQLAlchemy ORM with the following relationships:

- One-to-many between **User** and **Portfolio**.
- One-to-many between **Portfolio** and **Investment**.
- One-to-many between **Portfolio** and **Transaction**.
- One-to-many between **Company** and **Portfolio**, **Investment**, and **Transaction**.

## File Structure

```
my_project/
│
├── cli/
│   ├── __init__.py
│   ├── auth.py
│   ├── portfolio.py
│   ├── investment.py
│   ├── transaction.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── portfolio.py
│   ├── investment.py
│   ├── transaction.py
│   ├── company.py
│
├── db_setup.py
└── main.py
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.