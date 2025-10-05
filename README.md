# 💰 Personal Expense Tracker

Track your daily expenses, analyze spending habits, and visualize your financial data with this simple Streamlit app.

## Features

- Add new expenses with amount, date, category, and note
- View, filter, update, and delete expenses
- Download filtered expenses as CSV
- Visualize expenses by category and month
- See summary metrics (total spent, top category, highest expense)
- Interactive charts (bar, line) using Plotly

## How to Run

1. **Install dependencies:**
	```powershell
	pip install -r requirements.txt
	```
2. **Start the app:**
	```powershell
	streamlit run app.py
	```
3. Open the provided local URL in your browser.

## Assumptions

- Expenses are stored in a local SQLite database (`expenses.db`).
- Categories are predefined but can be edited during update.
- No authentication; all data is local and accessible to the user.
- Large expenses (over $100) are highlighted in red.

## Design Overview

- **Frontend:** Streamlit for UI, interactive widgets, and charts.
- **Backend:** SQLite via `db.py` for persistent storage.
- **Data Model:**
  - `id`: Auto-incremented integer
  - `amount`: Float
  - `date`: String (YYYY-MM-DD)
  - `category`: String
  - `note`: String

## Sample Inputs/Outputs

### Adding an Expense
| Amount | Date       | Category | Note         |
|--------|------------|----------|--------------|
| 25.50  | 2025-10-05 | food     | Lunch        |
| 120.00 | 2025-10-04 | travel   | Taxi fare    |

### Viewing Expenses (Filtered)
| id | amount | date       | category | note      |
|----|--------|------------|----------|-----------|
| 2  | 120.00 | 2025-10-04 | travel   | Taxi fare |
| 1  | 25.50  | 2025-10-05 | food     | Lunch     |

### Summary Metrics
- **Total Spent:** $145.50
- **Top Category:** travel
- **Highest Expense:** $120.00

## Author

Pabba Saiteja

## License

MIT
