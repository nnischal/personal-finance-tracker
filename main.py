import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]
    FORMAT = "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE) #pd = pandas module
            df.columns = df.columns.str.strip()  # Clean up the column names

            if df.empty:  # If the CSV is empty, re-create the structure
                df = pd.DataFrame(columns=cls.COLUMNS)
                df.to_csv(cls.CSV_FILE, index=False)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) #pd = module
            df.to_csv(cls.CSV_FILE, index=False) #df = dataframe
            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": datetime.strptime(date, cls.FORMAT).strftime("%d-%m-%Y"),
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)

        # Clean column names
        df.columns = df.columns.str.strip()
    
        if 'Date' not in df.columns:
            print("Error: 'Date' column not found in the CSV file.")
            return pd.DataFrame()  # Return an empty DataFrame if 'Date' is missing
        
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df.dropna(subset=["Date"], inplace=True) 
        
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)
        
        mask = (df["Date"]>= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print('No transaction found in the given date range')
        else:
            print(
                f"Transaction from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date": lambda x: x.strftime(cls.FORMAT)}
                )
            )
            
            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            
        return filtered_df
            
def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date:",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    
def plot_transactions(df):
    df.columns = df.columns.str.title()  # makes sure all headers are like 'Date', 'Amount', etc.
    #df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df.dropna(subset=["Date"], inplace=True)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.set_index("Date", inplace=True)
    
    income_df = (
        df[df["Category"] == "Income"]
        .resample("D") #daily resample
        .sum(numeric_only=True)
    )
    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum(numeric_only=True)
    )
    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expense over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    

def main():
    while True:
        print("\n 1. Add a new transaction")
        print("\n 2. View transactions and summary within a date range")
        print("\n 3. Exit")
        choice = input("Enter your choice (1-3):")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty:
                if input("Do you want to see a graph? [y/n]").lower() == "y":
                    plot_transactions(df)
                else:
                    print("No data available to plot a graph.!")
        elif choice == "3":
            print ("Exiting...!!!!!!!")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    main()