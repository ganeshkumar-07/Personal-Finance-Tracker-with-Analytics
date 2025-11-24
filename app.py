"""
Personal Finance Tracker - Web Application
Flask-based web interface
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from finance_tracker import FinanceTracker
from analytics import FinanceAnalytics
from datetime import datetime
import os
import base64
import io
import pandas as pd

# Set matplotlib backend before any imports
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Initialize tracker
tracker = FinanceTracker()


@app.route('/')
def index():
    """Home page with dashboard"""
    summary = tracker.get_summary()
    balance = tracker.get_balance()
    recent_transactions = tracker.get_transactions()[:10]  # Last 10 transactions
    
    # Prepare top 5 expense categories
    top_expenses = []
    if summary['expense_by_category']:
        sorted_expenses = sorted(summary['expense_by_category'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
        top_expenses = sorted_expenses
    
    return render_template('index.html', 
                         summary=summary, 
                         balance=balance,
                         transactions=recent_transactions,
                         top_expenses=top_expenses)


@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add a new transaction"""
    if request.method == 'POST':
        try:
            transaction_type = request.form.get('type')
            category = request.form.get('category')
            amount = float(request.form.get('amount'))
            description = request.form.get('description', '')
            date = request.form.get('date')
            
            if not date:
                date = None
            
            tracker.add_transaction(transaction_type, category, amount, description, date)
            flash(f'{transaction_type.capitalize()} added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    categories = tracker.get_categories()
    return render_template('add_transaction.html', categories=categories)


@app.route('/transactions')
def transactions():
    """View all transactions"""
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    transaction_type = request.args.get('type', '')
    category = request.args.get('category', '')
    
    filtered_transactions = tracker.get_transactions(
        start_date if start_date else None,
        end_date if end_date else None,
        transaction_type if transaction_type else None,
        category if category else None
    )
    
    categories = tracker.get_categories()
    return render_template('transactions.html', 
                         transactions=filtered_transactions,
                         categories=categories,
                         filters={
                             'start_date': start_date,
                             'end_date': end_date,
                             'type': transaction_type,
                             'category': category
                         })


@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete a transaction"""
    if tracker.delete_transaction(transaction_id):
        flash('Transaction deleted successfully!', 'success')
    else:
        flash('Transaction not found!', 'error')
    return redirect(url_for('transactions'))


@app.route('/summary')
def summary():
    """Financial summary page"""
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    summary_data = tracker.get_summary(
        start_date if start_date else None,
        end_date if end_date else None
    )
    
    return render_template('summary.html', 
                         summary=summary_data,
                         filters={
                             'start_date': start_date,
                             'end_date': end_date
                         })


@app.route('/analytics')
def analytics():
    """Analytics and reports page"""
    analytics_obj = FinanceAnalytics(tracker.transactions)
    report = analytics_obj.generate_report()
    
    return render_template('analytics.html', report=report)


@app.route('/chart/<chart_type>')
def generate_chart(chart_type):
    """Generate and return chart as image"""
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    analytics_obj = FinanceAnalytics(tracker.transactions)
    
    try:
        if chart_type == 'expense_pie':
            if analytics_obj.df.empty:
                return "No data available", 404
            
            expense_df = analytics_obj.df[analytics_obj.df['type'] == 'expense']
            if expense_df.empty:
                return "No expenses to visualize", 404
            
            category_totals = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            
            plt.figure(figsize=(10, 6))
            plt.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
            plt.title('Expenses by Category', fontsize=16, fontweight='bold')
            plt.axis('equal')
        
        elif chart_type == 'income_vs_expenses':
            if analytics_obj.df.empty:
                return "No data available", 404
            
            monthly_data = analytics_obj.df.groupby([analytics_obj.df['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
            
            if monthly_data.empty or len(monthly_data) == 0:
                return "No monthly data available", 404
            
            fig, ax = plt.subplots(figsize=(12, 6))
            x = range(len(monthly_data))
            width = 0.35
            
            income = monthly_data.get('income', pd.Series(dtype=float))
            expenses = monthly_data.get('expense', pd.Series(dtype=float))
            
            if not income.empty and len(income) > 0:
                ax.bar([i - width/2 for i in x], income.values, width, label='Income', color='#2ecc71')
            if not expenses.empty and len(expenses) > 0:
                ax.bar([i + width/2 for i in x], expenses.values, width, label='Expenses', color='#e74c3c')
            
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Amount (₹)', fontsize=12)
            ax.set_title('Monthly Income vs Expenses', fontsize=16, fontweight='bold')
            if len(monthly_data) > 0:
                ax.set_xticks(x)
                ax.set_xticklabels([str(period) for period in monthly_data.index], rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
        
        elif chart_type == 'spending_trend':
            if analytics_obj.df.empty:
                return "No data available", 404
            
            expense_df = analytics_obj.df[analytics_obj.df['type'] == 'expense'].copy()
            if expense_df.empty:
                return "No expenses to visualize", 404
            
            expense_df = expense_df.set_index('date')
            daily_expenses = expense_df.resample('D')['amount'].sum().fillna(0)
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            ax1.plot(daily_expenses.index, daily_expenses.values, color='#e74c3c', linewidth=2)
            ax1.fill_between(daily_expenses.index, daily_expenses.values, alpha=0.3, color='#e74c3c')
            ax1.set_title('Daily Spending Trend', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Amount (₹)', fontsize=12)
            ax1.grid(alpha=0.3)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            cumulative = daily_expenses.cumsum()
            ax2.plot(cumulative.index, cumulative.values, color='#3498db', linewidth=2)
            ax2.set_title('Cumulative Spending', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Date', fontsize=12)
            ax2.set_ylabel('Cumulative Amount (₹)', fontsize=12)
            ax2.grid(alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            plt.tight_layout()
        
        elif chart_type == 'category_comparison':
            if analytics_obj.df.empty:
                return "No data available", 404
            
            expense_df = analytics_obj.df[analytics_obj.df['type'] == 'expense']
            if expense_df.empty:
                return "No expenses to visualize", 404
            
            category_totals = expense_df.groupby('category')['amount'].sum().sort_values()
            
            plt.figure(figsize=(10, max(6, len(category_totals) * 0.5)))
            colors = plt.cm.Reds([0.4 + 0.6 * i / len(category_totals) for i in range(len(category_totals))])
            
            plt.barh(category_totals.index, category_totals.values, color=colors)
            plt.xlabel('Amount (₹)', fontsize=12)
            plt.title('Expenses by Category (Total)', fontsize=16, fontweight='bold')
            plt.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(category_totals.values):
                plt.text(v, i, f' ₹{v:,.2f}', va='center', fontweight='bold')
            
            plt.tight_layout()
        
        else:
            return "Invalid chart type", 404
        
        # Save to bytes buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close('all')  # Close all figures to free memory
        
        return send_file(img_buffer, mimetype='image/png')
    
    except Exception as e:
        import traceback
        error_msg = f"Error generating chart: {str(e)}"
        print(f"Chart generation error: {error_msg}")
        print(traceback.format_exc())
        plt.close('all')  # Ensure all figures are closed
        return error_msg, 500


@app.route('/api/balance')
def api_balance():
    """API endpoint for balance"""
    return jsonify({'balance': tracker.get_balance()})


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary"""
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    summary_data = tracker.get_summary(
        start_date if start_date else None,
        end_date if end_date else None
    )
    
    return jsonify(summary_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

