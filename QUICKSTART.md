# Quick Start Guide - Personal Finance Tracker Web Application

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Web Server

**Easy way (Recommended):**
- **Windows**: Double-click `run_server.bat`
- **Linux/Mac**: Run `./run_server.sh` or `python3 run_server.py`
- **Any OS**: Run `python run_server.py` (auto-installs missing packages)

**Alternative:**
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

That's it! You're ready to start tracking your finances! 🎉

## 📱 Using the Web Application

### Dashboard
- View your current balance, total income, and expenses at a glance
- See recent transactions
- Quick access to all features

### Adding Transactions
1. Click "Add Transaction" in the navigation
2. Select transaction type (Income or Expense)
3. Enter category, amount, description, and date
4. Click "Add Transaction"

### Viewing Transactions
- Click "Transactions" to see all your transactions
- Use filters to find specific transactions by date, type, or category
- Delete transactions directly from the list

### Financial Summary
- View detailed breakdowns of income and expenses
- See category-wise spending analysis
- Filter by date range

### Analytics
- View comprehensive statistics
- See visual charts and graphs
- Analyze spending patterns and trends

## 💡 Tips

- Use consistent category names for better analytics
- Regularly check your dashboard to stay on top of your finances
- Use the summary page to analyze specific time periods
- Explore the analytics section for insights into your spending habits

## 🔧 Troubleshooting

**Port already in use?**
- Change the port in `app.py`: `app.run(port=5001)`

**Charts not showing?**
- Make sure matplotlib and pandas are installed
- Check that you have transactions in your data

**Data not saving?**
- Ensure you have write permissions in the project directory
- Check that `transactions.csv` is not locked by another process

---

Enjoy tracking your finances! 💰📊

