"""
Personal Finance Tracker - Analytics Module
Provides data analysis and visualization capabilities
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict
import pandas as pd
from finance_tracker import Transaction


class FinanceAnalytics:
    """Analytics and visualization for finance data"""
    
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions
        self.df = self._create_dataframe()
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame"""
        if not self.transactions:
            return pd.DataFrame()
        
        data = []
        for t in self.transactions:
            data.append({
                'date': pd.to_datetime(t.date),
                'type': t.type,
                'category': t.category,
                'amount': t.amount,
                'description': t.description,
                'id': t.id
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values('date')
        return df
    
    def plot_expense_by_category(self, save_path: Optional[str] = None):
        """Create pie chart of expenses by category"""
        if self.df.empty:
            print("No transactions to visualize")
            return
        
        expense_df = self.df[self.df['type'] == 'expense']
        if expense_df.empty:
            print("No expenses to visualize")
            return
        
        category_totals = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        plt.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
        plt.title('Expenses by Category', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def plot_income_vs_expenses(self, save_path: Optional[str] = None):
        """Create bar chart comparing income and expenses"""
        if self.df.empty:
            print("No transactions to visualize")
            return
        
        monthly_data = self.df.groupby([self.df['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(monthly_data))
        width = 0.35
        
        income = monthly_data.get('income', pd.Series(dtype=float))
        expenses = monthly_data.get('expense', pd.Series(dtype=float))
        
        if not income.empty:
            ax.bar([i - width/2 for i in x], income.values, width, label='Income', color='#2ecc71')
        if not expenses.empty:
            ax.bar([i + width/2 for i in x], expenses.values, width, label='Expenses', color='#e74c3c')
        
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount (₹)', fontsize=12)
        ax.set_title('Monthly Income vs Expenses', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([str(period) for period in monthly_data.index], rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def plot_spending_trend(self, save_path: Optional[str] = None):
        """Create line chart showing spending trend over time"""
        if self.df.empty:
            print("No transactions to visualize")
            return
        
        expense_df = self.df[self.df['type'] == 'expense'].copy()
        if expense_df.empty:
            print("No expenses to visualize")
            return
        
        expense_df['cumulative'] = expense_df['amount'].cumsum()
        expense_df = expense_df.set_index('date')
        
        daily_expenses = expense_df.resample('D')['amount'].sum()
        daily_expenses = daily_expenses.fillna(0)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Daily spending
        ax1.plot(daily_expenses.index, daily_expenses.values, color='#e74c3c', linewidth=2)
        ax1.fill_between(daily_expenses.index, daily_expenses.values, alpha=0.3, color='#e74c3c')
        ax1.set_title('Daily Spending Trend', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Amount (₹)', fontsize=12)
        ax1.grid(alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Cumulative spending
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
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def plot_category_comparison(self, save_path: Optional[str] = None):
        """Create horizontal bar chart comparing expense categories"""
        if self.df.empty:
            print("No transactions to visualize")
            return
        
        expense_df = self.df[self.df['type'] == 'expense']
        if expense_df.empty:
            print("No expenses to visualize")
            return
        
        category_totals = expense_df.groupby('category')['amount'].sum().sort_values()
        
        plt.figure(figsize=(10, max(6, len(category_totals) * 0.5)))
        colors = plt.cm.Reds([0.4 + 0.6 * i / len(category_totals) for i in range(len(category_totals))])
        
        plt.barh(category_totals.index, category_totals.values, color=colors)
        plt.xlabel('Amount (₹)', fontsize=12)
        plt.title('Expenses by Category (Total)', fontsize=16, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(category_totals.values):
            plt.text(v, i, f' ₹{v:,.2f}', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def generate_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        if self.df.empty:
            return {"error": "No transactions available"}
        
        report = {
            'total_transactions': len(self.df),
            'date_range': {
                'start': str(self.df['date'].min().date()),
                'end': str(self.df['date'].max().date())
            },
            'income': {
                'total': float(self.df[self.df['type'] == 'income']['amount'].sum()),
                'average': float(self.df[self.df['type'] == 'income']['amount'].mean()) if len(self.df[self.df['type'] == 'income']) > 0 else 0,
                'count': len(self.df[self.df['type'] == 'income'])
            },
            'expenses': {
                'total': float(self.df[self.df['type'] == 'expense']['amount'].sum()),
                'average': float(self.df[self.df['type'] == 'expense']['amount'].mean()) if len(self.df[self.df['type'] == 'expense']) > 0 else 0,
                'count': len(self.df[self.df['type'] == 'expense'])
            },
            'balance': float(self.df[self.df['type'] == 'income']['amount'].sum() - 
                           self.df[self.df['type'] == 'expense']['amount'].sum()),
            'top_expense_categories': {}
        }
        
        expense_df = self.df[self.df['type'] == 'expense']
        if not expense_df.empty:
            top_categories = expense_df.groupby('category')['amount'].sum().nlargest(5)
            report['top_expense_categories'] = {cat: float(amt) for cat, amt in top_categories.items()}
        
        return report

