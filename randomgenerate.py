import csv
import os
import random
from datetime import datetime, timedelta

CSV_FILE = "finance_data.csv"
COLUMNS = ["Date", "Amount", "Category", "Description"]

categories = {
    "Income": ["Salary", "Bonus", "Freelance", "Dividends"],
    "Expense": ["Groceries", "Rent", "Utilities", "Dining Out", "Entertainment", "Transport", "Shopping"]
}

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_random_transactions(n=40):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 4, 1)

    # Check if the file exists and is empty
    file_exists = os.path.isfile(CSV_FILE)
    is_empty = not file_exists or os.stat(CSV_FILE).st_size == 0

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        
        # Write header if the file is new or empty
        if is_empty:
            writer.writeheader()

        for _ in range(n):
            category_type = random.choice(list(categories.keys()))
            category = random.choice(categories[category_type])
            amount = round(random.uniform(50, 4000), 2) if category_type == "Income" else round(random.uniform(5, 1000), 2)
            date = random_date(start_date, end_date).strftime("%d-%m-%Y")
            description = f"{category} payment"
            
            writer.writerow({
                "Date": date,
                "Amount": amount,
                "Category": category_type,
                "Description": description
            })
    print(f"{n} random transactions added to {CSV_FILE}.")

generate_random_transactions(40)
