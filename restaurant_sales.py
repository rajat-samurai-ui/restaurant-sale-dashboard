"""
PS 72 - Restaurant Sales Dashboard
Reads restaurant_sales.csv with Pandas, computes Sales = Quantity x Price,
and uses GroupBy to show sales by category, by date and top items,
with charts. Invalid rows are skipped with a warning.

Usage:  python restaurant_sales.py [csv_file]
"""

import sys
import pandas as pd
import matplotlib

# Use a non-GUI backend automatically if no display is available
try:
    import tkinter  # noqa: F401
except ImportError:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEFAULT_FILE = "restaurant_sales.csv"
REQUIRED_COLUMNS = ["Date", "Item", "Category", "Quantity", "Price"]


# --------------------------------------------------------------------------
# Loading and validation
# --------------------------------------------------------------------------
def validate_row(row):
    """Return an error message if the row is invalid, otherwise None."""
    for col in ("Date", "Item", "Category"):
        if pd.isna(row[col]) or str(row[col]).strip() == "":
            return f"{col} is missing."

    if pd.isna(pd.to_datetime(row["Date"], format="%Y-%m-%d", errors="coerce")):
        return "Date must be in YYYY-MM-DD format."

    try:
        qty = float(row["Quantity"])
    except (TypeError, ValueError):
        return "Quantity must be a number."
    if qty <= 0 or qty != int(qty):
        return "Quantity must be a positive whole number."

    try:
        price = float(row["Price"])
    except (TypeError, ValueError):
        return "Price must be a number."
    if price < 0:
        return "Price cannot be negative."

    return None


def load_sales(filename):
    """Load the CSV, skip invalid rows and add a Sales column.
    Returns a DataFrame, or None if the file cannot be used."""
    try:
        raw = pd.read_csv(filename, dtype=str, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{filename}' is empty.")
        return None

    raw.columns = [c.strip() for c in raw.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        print(f"Error: Missing column(s): {', '.join(missing)}")
        return None

    valid_rows = []
    for idx, row in raw.iterrows():
        file_row = idx + 2  # +1 for header line, +1 because idx starts at 0
        problem = validate_row(row)
        if problem:
            print(f"Warning: Row {file_row} skipped - {problem}")
        else:
            valid_rows.append(idx)

    df = raw.loc[valid_rows].copy()
    if df.empty:
        print("Error: No valid rows found in the file.")
        return None

    df["Item"] = df["Item"].str.strip()
    df["Category"] = df["Category"].str.strip()
    df["Date"] = df["Date"].str.strip()
    df["Quantity"] = df["Quantity"].astype(float).astype(int)
    df["Price"] = df["Price"].astype(float)
    df["Sales"] = df["Quantity"] * df["Price"]  # Sales = Quantity x Price
    return df


# --------------------------------------------------------------------------
# Reports (all use GroupBy)
# --------------------------------------------------------------------------
def money(value):
    return f"Rs. {value:,.0f}".replace(",", "")


def sales_by_category(df):
    return df.groupby("Category")["Sales"].sum().sort_values(ascending=False)


def sales_by_item(df):
    return df.groupby("Item").agg(Quantity=("Quantity", "sum"),
                                  Sales=("Sales", "sum"))


def sales_by_date(df):
    return df.groupby("Date")["Sales"].sum().sort_index()


def show_category_report(df):
    print("\n--- Sales by Category ---")
    cat = sales_by_category(df)
    for name, value in cat.items():
        print(f"{name:<8}: {money(value)}")
    print(f"Total sales: {money(df['Sales'].sum())}")


def show_top_items(df):
    print("\n--- Top Items ---")
    items = sales_by_item(df)
    top_qty = items["Quantity"].idxmax()
    top_rev = items["Sales"].idxmax()
    qty = int(items.loc[top_qty, "Quantity"])
    unit = "unit" if qty == 1 else "units"
    print(f"Top item by quantity: {top_qty} ({qty} {unit})")
    print(f"Top item by revenue: {top_rev} ({money(items.loc[top_rev, 'Sales'])})")


def show_daily_sales(df):
    print("\n--- Daily Sales ---")
    daily = sales_by_date(df)
    for day, value in daily.items():
        print(f"{day} : {money(value)}")
    print(f"Best day: {daily.idxmax()}")


# --------------------------------------------------------------------------
# Charts
# --------------------------------------------------------------------------
def show_charts(df):
    cat = sales_by_category(df)
    daily = sales_by_date(df)
    items = sales_by_item(df).sort_values("Sales", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Restaurant Sales Dashboard", fontsize=14, fontweight="bold")

    axes[0].bar(cat.index, cat.values, color="#4C72B0")
    axes[0].set_title("Sales by Category")
    axes[0].set_ylabel("Sales (Rs.)")

    axes[1].plot(daily.index, daily.values, marker="o", color="#DD8452")
    axes[1].set_title("Daily Sales")
    axes[1].set_ylabel("Sales (Rs.)")
    axes[1].tick_params(axis="x", rotation=30)

    axes[2].barh(items.index[::-1], items["Sales"].values[::-1], color="#55A868")
    axes[2].set_title("Revenue by Item")
    axes[2].set_xlabel("Sales (Rs.)")

    plt.tight_layout()
    plt.savefig("sales_dashboard.png", dpi=120)
    print("Charts saved as sales_dashboard.png")
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


# --------------------------------------------------------------------------
# Menu
# --------------------------------------------------------------------------
def menu(df):
    while True:
        print("\n===== Restaurant Sales Dashboard =====")
        print("1. Sales by category")
        print("2. Top items")
        print("3. Daily sales")
        print("4. Show charts")
        print("5. Exit")
        try:
            choice = input("Enter choice (1-5): ").strip()
        except EOFError:
            break

        if choice == "1":
            show_category_report(df)
        elif choice == "2":
            show_top_items(df)
        elif choice == "3":
            show_daily_sales(df)
        elif choice == "4":
            show_charts(df)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input(f"CSV file name [{DEFAULT_FILE}]: ").strip() or DEFAULT_FILE

    df = load_sales(filename)
    if df is None:
        return
    menu(df)


if __name__ == "__main__":
    main()
