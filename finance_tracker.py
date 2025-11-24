"""
Personal Finance Tracker - Core Module
Handles transaction management and data storage
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    """Represents a financial transaction"""
    date: str
    type: str  # 'income' or 'expense'
    category: str
    amount: float
    description: str
    id: Optional[int] = None

    def __post_init__(self):
        if self.id is None:
            self.id = int(datetime.now().timestamp() * 1000)


class FinanceTracker:
    """Main class for managing personal finances"""
    
    def __init__(self, data_file: str = "transactions.csv"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self._load_transactions()
    
    def _load_transactions(self):
        """Load transactions from CSV file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    transaction = Transaction(
                        id=int(row['id']),
                        date=row['date'],
                        type=row['type'],
                        category=row['category'],
                        amount=float(row['amount']),
                        description=row['description']
                    )
                    self.transactions.append(transaction)
        except Exception as e:
            print(f"Error loading transactions: {e}")
    
    def _save_transactions(self):
        """Save transactions to CSV file"""
        if not self.transactions:
            return
        
        fieldnames = ['id', 'date', 'type', 'category', 'amount', 'description']
        with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(asdict(transaction))
    
    def add_transaction(self, transaction_type: str, category: str, 
                       amount: float, description: str, date: Optional[str] = None):
        """Add a new transaction"""
        if transaction_type.lower() not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        transaction = Transaction(
            date=date,
            type=transaction_type.lower(),
            category=category,
            amount=amount,
            description=description
        )
        
        self.transactions.append(transaction)
        self._save_transactions()
        return transaction
    
    def delete_transaction(self, transaction_id: int):
        """Delete a transaction by ID"""
        original_count = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        
        if len(self.transactions) < original_count:
            self._save_transactions()
            return True
        return False
    
    def get_transactions(self, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None,
                        transaction_type: Optional[str] = None,
                        category: Optional[str] = None) -> List[Transaction]:
        """Get filtered transactions"""
        filtered = self.transactions.copy()
        
        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]
        
        if transaction_type:
            filtered = [t for t in filtered if t.type == transaction_type.lower()]
        
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
        
        return sorted(filtered, key=lambda x: x.date, reverse=True)
    
    def get_balance(self) -> float:
        """Calculate current balance"""
        income = sum(t.amount for t in self.transactions if t.type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.type == 'expense')
        return income - expenses
    
    def get_summary(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> Dict:
        """Get financial summary"""
        transactions = self.get_transactions(start_date, end_date)
        
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expenses
        
        # Category breakdown
        expense_by_category = {}
        income_by_category = {}
        
        for t in transactions:
            if t.type == 'expense':
                expense_by_category[t.category] = expense_by_category.get(t.category, 0) + t.amount
            else:
                income_by_category[t.category] = income_by_category.get(t.category, 0) + t.amount
        
        return {
            'total_income': income,
            'total_expenses': expenses,
            'balance': balance,
            'transaction_count': len(transactions),
            'expense_by_category': expense_by_category,
            'income_by_category': income_by_category
        }
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set()
        for t in self.transactions:
            categories.add(t.category)
        return sorted(list(categories))

