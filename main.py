"""
Personal Finance Tracker - Main Application
Command-line interface for managing personal finances
"""

import sys
from datetime import datetime
from finance_tracker import FinanceTracker, Transaction
from analytics import FinanceAnalytics


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print(" " * 15 + "PERSONAL FINANCE TRACKER")
    print("="*60 + "\n")


def print_menu():
    """Print main menu options"""
    print("Main Menu:")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Summary")
    print("5. View Balance")
    print("6. Delete Transaction")
    print("7. Analytics & Reports")
    print("8. Generate Charts")
    print("9. Exit")
    print()


def add_transaction(tracker: FinanceTracker, transaction_type: str):
    """Add a new transaction"""
    print(f"\n--- Add {transaction_type.title()} ---")
    
    try:
        category = input(f"Category: ").strip()
        if not category:
            print("Category cannot be empty!")
            return
        
        amount_str = input("Amount ($): ").strip()
        amount = float(amount_str)
        if amount <= 0:
            print("Amount must be positive!")
            return
        
        description = input("Description: ").strip()
        if not description:
            description = f"{transaction_type.title()} - {category}"
        
        date_str = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        date = None
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                date = date_str
            except ValueError:
                print("Invalid date format! Using today's date.")
        
        transaction = tracker.add_transaction(transaction_type, category, amount, description, date)
        print(f"\n✓ {transaction_type.title()} added successfully!")
        print(f"  ID: {transaction.id}")
        print(f"  Date: {transaction.date}")
        print(f"  Category: {transaction.category}")
        print(f"  Amount: ${transaction.amount:.2f}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def view_transactions(tracker: FinanceTracker):
    """View all transactions"""
    print("\n--- Transactions ---")
    
    transactions = tracker.get_transactions()
    
    if not transactions:
        print("No transactions found.")
        return
    
    print(f"\nTotal Transactions: {len(transactions)}\n")
    print(f"{'ID':<12} {'Date':<12} {'Type':<10} {'Category':<20} {'Amount':<12} {'Description'}")
    print("-" * 90)
    
    for t in transactions:
        amount_str = f"${t.amount:.2f}"
        if t.type == 'expense':
            amount_str = f"-${t.amount:.2f}"
        print(f"{t.id:<12} {t.date:<12} {t.type.capitalize():<10} {t.category:<20} {amount_str:<12} {t.description}")
    
    print()


def view_summary(tracker: FinanceTracker):
    """View financial summary"""
    print("\n--- Financial Summary ---")
    
    start_date = input("Start date (YYYY-MM-DD, press Enter for all): ").strip()
    end_date = input("End date (YYYY-MM-DD, press Enter for all): ").strip()
    
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    
    summary = tracker.get_summary(start_date, end_date)
    
    print(f"\n{'='*50}")
    print(f"Total Income:     ${summary['total_income']:,.2f}")
    print(f"Total Expenses:   ${summary['total_expenses']:,.2f}")
    print(f"Balance:          ${summary['balance']:,.2f}")
    print(f"Transactions:     {summary['transaction_count']}")
    print(f"{'='*50}\n")
    
    if summary['expense_by_category']:
        print("Expenses by Category:")
        print("-" * 30)
        for category, amount in sorted(summary['expense_by_category'].items(), 
                                       key=lambda x: x[1], reverse=True):
            print(f"  {category:<20} ${amount:,.2f}")
        print()
    
    if summary['income_by_category']:
        print("Income by Category:")
        print("-" * 30)
        for category, amount in sorted(summary['income_by_category'].items(), 
                                      key=lambda x: x[1], reverse=True):
            print(f"  {category:<20} ${amount:,.2f}")
        print()


def view_balance(tracker: FinanceTracker):
    """View current balance"""
    print("\n--- Current Balance ---")
    balance = tracker.get_balance()
    
    if balance >= 0:
        print(f"\nCurrent Balance: ${balance:,.2f} (Positive)")
    else:
        print(f"\nCurrent Balance: ${balance:,.2f} (Negative)")
    print()


def delete_transaction(tracker: FinanceTracker):
    """Delete a transaction"""
    print("\n--- Delete Transaction ---")
    
    view_transactions(tracker)
    
    try:
        transaction_id = input("Enter transaction ID to delete (or 'cancel'): ").strip()
        if transaction_id.lower() == 'cancel':
            return
        
        transaction_id = int(transaction_id)
        
        if tracker.delete_transaction(transaction_id):
            print(f"\n✓ Transaction {transaction_id} deleted successfully!")
        else:
            print(f"\n✗ Transaction {transaction_id} not found!")
            
    except ValueError:
        print("Invalid transaction ID!")
    except Exception as e:
        print(f"An error occurred: {e}")


def analytics_menu(tracker: FinanceTracker):
    """Analytics and reports menu"""
    analytics = FinanceAnalytics(tracker.transactions)
    
    while True:
        print("\n--- Analytics & Reports ---")
        print("1. View Analytics Report")
        print("2. Expense by Category (Pie Chart)")
        print("3. Income vs Expenses (Bar Chart)")
        print("4. Spending Trend (Line Chart)")
        print("5. Category Comparison (Bar Chart)")
        print("6. Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            report = analytics.generate_report()
            if 'error' in report:
                print(f"\n{report['error']}")
            else:
                print("\n" + "="*50)
                print("ANALYTICS REPORT")
                print("="*50)
                print(f"Total Transactions: {report['total_transactions']}")
                print(f"Date Range: {report['date_range']['start']} to {report['date_range']['end']}")
                print(f"\nIncome:")
                print(f"  Total: ${report['income']['total']:,.2f}")
                print(f"  Average: ${report['income']['average']:,.2f}")
                print(f"  Count: {report['income']['count']}")
                print(f"\nExpenses:")
                print(f"  Total: ${report['expenses']['total']:,.2f}")
                print(f"  Average: ${report['expenses']['average']:,.2f}")
                print(f"  Count: {report['expenses']['count']}")
                print(f"\nBalance: ${report['balance']:,.2f}")
                if report['top_expense_categories']:
                    print(f"\nTop Expense Categories:")
                    for cat, amt in report['top_expense_categories'].items():
                        print(f"  {cat}: ${amt:,.2f}")
                print("="*50)
        
        elif choice == '2':
            save = input("Save chart? (y/n): ").strip().lower()
            save_path = "expense_by_category.png" if save == 'y' else None
            analytics.plot_expense_by_category(save_path)
        
        elif choice == '3':
            save = input("Save chart? (y/n): ").strip().lower()
            save_path = "income_vs_expenses.png" if save == 'y' else None
            analytics.plot_income_vs_expenses(save_path)
        
        elif choice == '4':
            save = input("Save chart? (y/n): ").strip().lower()
            save_path = "spending_trend.png" if save == 'y' else None
            analytics.plot_spending_trend(save_path)
        
        elif choice == '5':
            save = input("Save chart? (y/n): ").strip().lower()
            save_path = "category_comparison.png" if save == 'y' else None
            analytics.plot_category_comparison(save_path)
        
        elif choice == '6':
            break
        
        else:
            print("Invalid option!")


def main():
    """Main application loop"""
    tracker = FinanceTracker()
    
    print_header()
    
    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            add_transaction(tracker, 'income')
        
        elif choice == '2':
            add_transaction(tracker, 'expense')
        
        elif choice == '3':
            view_transactions(tracker)
        
        elif choice == '4':
            view_summary(tracker)
        
        elif choice == '5':
            view_balance(tracker)
        
        elif choice == '6':
            delete_transaction(tracker)
        
        elif choice == '7':
            analytics_menu(tracker)
        
        elif choice == '8':
            analytics = FinanceAnalytics(tracker.transactions)
            print("\nGenerating all charts...")
            analytics.plot_expense_by_category("expense_by_category.png")
            analytics.plot_income_vs_expenses("income_vs_expenses.png")
            analytics.plot_spending_trend("spending_trend.png")
            analytics.plot_category_comparison("category_comparison.png")
            print("\n✓ All charts generated!")
        
        elif choice == '9':
            print("\nThank you for using Personal Finance Tracker!")
            print("Goodbye!\n")
            break
        
        else:
            print("Invalid option! Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)

