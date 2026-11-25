# Restaurant Sales Dashboard (PS 72)

A Python 3 console program that reads `restaurant_sales.csv` with Pandas, calculates
`Sales = Quantity x Price`, and uses `GroupBy` to report sales by category, item and date,
with Matplotlib charts. Invalid rows are skipped with a warning.

## Requirements
- Python 3
- pandas, matplotlib (`pip install pandas matplotlib`)

## How to run
```
python restaurant_sales.py                      # asks for the file name
python restaurant_sales.py restaurant_sales.csv # pass the file directly
```

## Menu
1. Sales by category
2. Top items (by quantity and by revenue)
3. Daily sales (with best day)
4. Show charts (also saved as `sales_dashboard.png`)
5. Exit

## CSV format
`Date,Item,Category,Quantity,Price` (Date as YYYY-MM-DD)

## Test cases
| # | Input | Result |
|---|-------|--------|
| 1 | Sample file, menu 1 | Main Rs. 6300, Starter Rs. 4840, Dessert Rs. 3600, Total Rs. 14740 |
| 2 | One-row file, menu 2 | Top by quantity: Paneer Tikka (1 unit); by revenue: Rs. 220 |
| 3a | Extra row `Lassi,Drink,five,60` | Warning: Row 8 skipped - Quantity must be a number. |
| 3b | `sales2025.csv` missing | Error: File 'sales2025.csv' not found. |
| 4 | Sample file, menus 2 and 3 | Top qty Gulab Jamun (45 units), top revenue Paneer Tikka (Rs. 4840), 10-01 Rs. 7700, 10-02 Rs. 7040, best day 2026-10-01 |

## Concepts used
Pandas, Matplotlib, CSV handling, GroupBy, input validation.
