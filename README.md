# Personal Finance Tracker with Analytics

A comprehensive Python-based personal finance tracking application with advanced analytics and visualization capabilities. Available as both a **web application** (HTML/CSS) and a **command-line interface**.

## Features

### Core Functionality
- **Income & Expense Tracking**: Add, view, and manage financial transactions
- **Category Management**: Organize transactions by custom categories
- **Balance Calculation**: Real-time balance tracking
- **Transaction History**: View all transactions with filtering options
- **Data Persistence**: All data stored in CSV format for easy access

### Analytics & Visualization
- **Financial Summary**: Comprehensive overview of income, expenses, and balance
- **Category Analysis**: Breakdown of spending by category
- **Interactive Charts**:
  - Expense distribution (Pie Chart)
  - Monthly Income vs Expenses (Bar Chart)
  - Spending trends over time (Line Chart)
  - Category comparison (Horizontal Bar Chart)
- **Analytics Reports**: Detailed statistical analysis

## Installation

1. **Clone or download this repository**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 Web Application (Recommended)

The web application provides a beautiful, modern interface with HTML and CSS styling.

**Start the web server (choose one method):**

**Method 1: Using the run server script (Recommended)**
- **Windows**: Double-click `run_server.bat` or run `run_server.bat` in command prompt
- **Linux/Mac**: Run `chmod +x run_server.sh && ./run_server.sh` or `python3 run_server.py`
- **Cross-platform**: Run `python run_server.py` (automatically checks and installs dependencies)

**Method 2: Direct Python command**
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

> **Note**: The `run_server.py` script automatically checks for missing dependencies and installs them if needed.

**Web Application Features:**
- Beautiful, responsive dashboard
- Easy-to-use forms for adding transactions
- Interactive transaction filtering
- Real-time financial summaries
- Visual analytics with charts
- Modern, mobile-friendly design

**Web Pages:**
- **Dashboard** (`/`) - Overview with balance, summary cards, and recent transactions
- **Add Transaction** (`/add_transaction`) - Form to add income or expenses
- **Transactions** (`/transactions`) - View and filter all transactions
- **Summary** (`/summary`) - Financial summary with date filtering
- **Analytics** (`/analytics`) - Detailed analytics and visualization charts

### 💻 Command-Line Interface

For users who prefer a terminal-based interface:

```bash
python main.py
```

### Main Menu Options

1. **Add Income**: Record income transactions
2. **Add Expense**: Record expense transactions
3. **View Transactions**: Display all transactions
4. **View Summary**: Get financial summary with optional date filtering
5. **View Balance**: Check current balance
6. **Delete Transaction**: Remove a transaction by ID
7. **Analytics & Reports**: Access analytics menu with various reports and charts
8. **Generate Charts**: Create all visualization charts at once
9. **Exit**: Close the application

### Example Usage

#### Adding a Transaction
```
Select an option: 2
Category: Groceries
Amount ($): 150.50
Description: Weekly grocery shopping
Date (YYYY-MM-DD, press Enter for today): 2024-01-15
```

#### Viewing Summary
```
Select an option: 4
Start date (YYYY-MM-DD, press Enter for all): 2024-01-01
End date (YYYY-MM-DD, press Enter for all): 2024-01-31
```

#### Generating Charts
Charts can be generated individually from the Analytics menu or all at once using option 8. Charts can be saved as PNG files for later reference.

## Project Structure

```
.
├── app.py                  # Flask web application
├── main.py                 # CLI application entry point
├── finance_tracker.py      # Core finance tracking logic
├── analytics.py            # Analytics and visualization module
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates for web app
│   ├── base.html
│   ├── index.html
│   ├── add_transaction.html
│   ├── transactions.html
│   ├── summary.html
│   └── analytics.html
├── static/                # Static files (CSS, JS, images)
│   └── style.css
└── transactions.csv       # Data storage (created automatically)
```

## Data Storage

All transactions are stored in `transactions.csv` with the following structure:
- `id`: Unique transaction identifier
- `date`: Transaction date (YYYY-MM-DD)
- `type`: Transaction type (income/expense)
- `category`: Transaction category
- `amount`: Transaction amount
- `description`: Transaction description

## Features in Detail

### Transaction Management
- Add income and expense transactions
- Automatic date assignment (current date if not specified)
- Category-based organization
- Transaction deletion by ID
- Filter transactions by date, type, or category

### Analytics Capabilities
- **Summary Statistics**: Total income, expenses, balance, and transaction counts
- **Category Breakdown**: See where money is being spent or earned
- **Trend Analysis**: Track spending patterns over time
- **Visual Reports**: Multiple chart types for different insights

### Visualization Charts
1. **Expense by Category (Pie Chart)**: Visual distribution of expenses
2. **Income vs Expenses (Bar Chart)**: Monthly comparison
3. **Spending Trend (Line Chart)**: Daily and cumulative spending patterns
4. **Category Comparison (Bar Chart)**: Total spending by category

## Requirements

- Python 3.7 or higher
- Flask >= 2.3.0 (for web application)
- matplotlib >= 3.7.0
- pandas >= 2.0.0

## Tips

- Use consistent category names for better analytics
- Regularly review your spending trends to identify patterns
- Export charts periodically to track your financial progress
- Use date filtering in summaries to analyze specific time periods

## Future Enhancements

Potential features for future versions:
- Budget setting and tracking
- Recurring transaction support
- Export to Excel/PDF
- Data backup and restore
- Multiple account support
- Investment tracking

## License

This project is open source and available for personal and educational use.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Happy Tracking!** 📊💰

