import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'transactions': [], 'budgets': {}}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)

def add_transaction(data):
    amount = float(input("Amount: "))
    category = input("Category: ").strip()
    note = input("Note (optional): ").strip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data['transactions'].append({
        'amount': amount,
        'category': category,
        'note': note,
        'timestamp': timestamp
    })
    print("Transaction added.")
    save_data(data)

def set_budget(data):
    category = input("Category: ").strip()
    amount = float(input("Set budget: "))
    data['budgets'][category] = amount
    print(f"Budget for '{category}' set to {amount}.")
    save_data(data)

def view_summary(data):
    summary = {}
    for txn in data['transactions']:
        cat = txn['category']
        summary[cat] = summary.get(cat, 0) + txn['amount']

    print("\n=== Budget Summary ===")
    for cat, spent in summary.items():
        budget = data['budgets'].get(cat, 0)
        remaining = budget - spent
        print(f"{cat}: Spent = {spent}, Budget = {budget}, Remaining = {remaining}")
    print()

def view_history(data):
    print("\n=== Transaction History ===")
    for txn in data['transactions']:
        print(f"[{txn['timestamp']}] {txn['category']} - {txn['amount']} ({txn['note']})")
    print()

def main():
    data = load_data()
    while True:
        print("\nCommands: add | budget | summary | history | exit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == 'add':
            add_transaction(data)
        elif cmd == 'budget':
            set_budget(data)
        elif cmd == 'summary':
            view_summary(data)
        elif cmd == 'history':
            view_history(data)
        elif cmd == 'exit':
            break
        else:
            print("Invalid command. Try again.")

if __name__ == '__main__':
    main()
