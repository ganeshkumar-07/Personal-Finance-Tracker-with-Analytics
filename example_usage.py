"""
Example usage of the Personal Finance Tracker
This script demonstrates how to use the FinanceTracker programmatically
"""

from finance_tracker import FinanceTracker
from analytics import FinanceAnalytics
from datetime import datetime, timedelta

def example_usage():
    """Demonstrate basic usage of the finance tracker"""
    
    # Create a tracker instance (using a demo data file)
    tracker = FinanceTracker("example_transactions.csv")
    
    print("=== Personal Finance Tracker - Example Usage ===\n")
    
    # Add some sample transactions
    print("1. Adding sample transactions...")
    
    # Income
    tracker.add_transaction('income', 'Salary', 5000.00, 'Monthly salary', '2024-01-01')
    tracker.add_transaction('income', 'Freelance', 800.00, 'Web design project', '2024-01-15')
    tracker.add_transaction('income', 'Salary', 5000.00, 'Monthly salary', '2024-02-01')
    
    # Expenses
    tracker.add_transaction('expense', 'Rent', 1200.00, 'Monthly rent', '2024-01-05')
    tracker.add_transaction('expense', 'Groceries', 350.00, 'Weekly groceries', '2024-01-10')
    tracker.add_transaction('expense', 'Transportation', 150.00, 'Gas and public transport', '2024-01-12')
    tracker.add_transaction('expense', 'Entertainment', 200.00, 'Movies and dining', '2024-01-18')
    tracker.add_transaction('expense', 'Rent', 1200.00, 'Monthly rent', '2024-02-05')
    tracker.add_transaction('expense', 'Groceries', 320.00, 'Weekly groceries', '2024-02-10')
    tracker.add_transaction('expense', 'Utilities', 180.00, 'Electricity and water', '2024-02-12')
    
    print("   ✓ Added sample transactions\n")
    
    # View balance
    print("2. Current Balance:")
    balance = tracker.get_balance()
    print(f"   ${balance:,.2f}\n")
    
    # Get summary
    print("3. Financial Summary:")
    summary = tracker.get_summary()
    print(f"   Total Income:   ${summary['total_income']:,.2f}")
    print(f"   Total Expenses: ${summary['total_expenses']:,.2f}")
    print(f"   Balance:        ${summary['balance']:,.2f}")
    print(f"   Transactions:   {summary['transaction_count']}\n")
    
    # Category breakdown
    print("4. Expense Breakdown by Category:")
    for category, amount in sorted(summary['expense_by_category'].items(), 
                                   key=lambda x: x[1], reverse=True):
        print(f"   {category:<20} ${amount:,.2f}")
    print()
    
    # Analytics
    print("5. Generating analytics report...")
    analytics = FinanceAnalytics(tracker.transactions)
    report = analytics.generate_report()
    
    print(f"   Date Range: {report['date_range']['start']} to {report['date_range']['end']}")
    print(f"   Average Expense: ${report['expenses']['average']:,.2f}")
    print(f"   Average Income: ${report['income']['average']:,.2f}\n")
    
    # Generate charts
    print("6. Generating visualization charts...")
    analytics.plot_expense_by_category("example_expense_by_category.png")
    analytics.plot_income_vs_expenses("example_income_vs_expenses.png")
    analytics.plot_spending_trend("example_spending_trend.png")
    analytics.plot_category_comparison("example_category_comparison.png")
    print("   ✓ Charts saved as PNG files\n")
    
    print("=== Example completed! ===")
    print("\nNote: This example created 'example_transactions.csv' and chart files.")
    print("You can delete these files or use them as reference.")

if __name__ == "__main__":
    example_usage()

