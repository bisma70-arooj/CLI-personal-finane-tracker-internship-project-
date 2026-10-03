#--- CLI PERSONAL FINANCE TRACKER (INTERNSHIP PROJECT)-----

import sys 
import pandas as pd

transactions = []


def get_positive_number(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Please enter a number greater than zero!")
                continue
            return amount
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def add_transaction(trans_type):
    print(f"\n--- Add {trans_type.capitalize()} ---")

    amount = get_positive_number("Enter the amount ($): ")
    category = (
        input(
            "Enter the category (e.g. salary, food, transport, utilities,"
            " rent, bills, etc): "
        )
        .strip()
        .capitalize()
    )
    description = input("Enter the description: ").strip()

    if not category:
        category = "Uncategorized"

    if not description:
        description = "No description provided"

    transaction = {
        "type": trans_type.lower(),
        "amount": amount,
        "category": category,
        "description": description,
    }

    transactions.append(transaction)
    print(
        f"[SUCCESS] {trans_type.capitalize()} of ${amount:.2f} added"
        " successfully!"
    )


def display_transactions(trans_list):
    if not trans_list:
        print("\nNo transactions found.")
        return

    df = pd.DataFrame(trans_list)

    # Format output using Pandas
    formatted_df = df.copy()
    formatted_df["type"] = formatted_df["type"].str.capitalize()
    formatted_df["amount"] = formatted_df.apply(
        lambda row: (
            f"+${row['amount']:.2f}"
            if row["type"].lower() == "income"
            else f"-${row['amount']:.2f}"
        ),
        axis=1,
    )

    formatted_df = formatted_df.rename(
        columns={
            "type": "Type",
            "amount": "Amount($)",
            "category": "Category",
            "description": "Description",
        }
    )

    formatted_df.index = range(1, len(formatted_df) + 1)
    formatted_df.index.name = "#"

    print("\n" + formatted_df.to_string())


def filter_by_category():
    if not transactions:
        print("\n[WARNING] No transactions recorded yet.")
        return

    category_to_filter = (
        input("\nEnter category to filter by: ").strip().capitalize()
    )

    filtered = [t for t in transactions if t["category"] == category_to_filter]

    if filtered:
        print(f"\n--- Transactions for Category: '{category_to_filter}' ---")
        display_transactions(filtered)
    else:
        print(
            f"\n[ERROR] No transactions found under category"
            f" '{category_to_filter}'."
        )


def generate_summary():
    if not transactions:
        print("\n[WARNING] No transactions available to summarize.")
        return

    total_income = sum(
        t["amount"] for t in transactions if t["type"] == "income"
    )
    total_expense = sum(
        t["amount"] for t in transactions if t["type"] == "expense"
    )
    net_balance = total_income - total_expense

    print("\n" + " FINANCIAL SUMMARY REPORT ".center(45, "="))
    print(f" Total Income   :  ${total_income:>10.2f}")
    print(f" Total Expense  :  ${total_expense:>10.2f}")
    print("-" * 45)

    if net_balance >= 0:
        print(f" Net Balance    :  ${net_balance:>10.2f} (Savings)")
    else:
        print(f" Net Balance    : -${abs(net_balance):>10.2f} (Deficit)")

    # Category Breakdown
    print("\n--- Category Breakdown ---")
    categories = set(t["category"] for t in transactions)

    for cat in categories:
        cat_income = sum(
            t["amount"]
            for t in transactions
            if t["category"] == cat and t["type"] == "income"
        )
        cat_expense = sum(
            t["amount"]
            for t in transactions
            if t["category"] == cat and t["type"] == "expense"
        )
        net_cat = cat_income - cat_expense

        print(
            f"* {cat:<15}: +${cat_income:<8.2f} | -${cat_expense:<8.2f} | Net:"
            f" ${net_cat:.2f}"
        )

    print("=" * 45)


def main():
    while True:
        print("\n" + " PERSONAL FINANCE TRACKER ".center(40, "*"))
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Filter Transactions by Category")
        print("5. View Financial Summary Report")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            add_transaction("income")
        elif choice == "2":
            add_transaction("expense")
        elif choice == "3":
            print("\n--- All Transactions ---")
            display_transactions(transactions)
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            generate_summary()
        elif choice == "6":
            print("\nThank you for using Personal Finance Tracker. Goodbye!")
            break
        else:
            print(
                "\n[ERROR] Invalid choice! Please enter a number between 1"
                " and 6."
            )


if __name__ == "__main__":
    main()