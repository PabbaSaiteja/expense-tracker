import streamlit as st
import pandas as pd
from datetime import date
import db
import plotly.express as px


st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Initialize database
db.init_db()

st.title("Personal Expense Tracker")

# ---------------- Sidebar Menu -----------------
menu = ["Add Expense", "View Expenses", "Summary"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Helpers -----------------
def highlight_large(val):
    """Highlight large expenses in red."""
    color = "red" if val > 100 else ""  
    return f"color: {color}"

def get_top_category(df):
    if df.empty:
        return "-"
    return df.groupby("category")["amount"].sum().idxmax()

def get_highest_expense(df):
    if df.empty:
        return 0
    return df["amount"].max()

# ---------------- Add Expense -----------------
if choice == "Add Expense":
    st.header(" Add a New Expense")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        expense_date = st.date_input("Date", date.today())
    with col2:
        category = st.selectbox("Category", ["food", "travel", "bills", "shopping", "other"])
        note = st.text_input("Note")

    if st.button("Add Expense"):
        db.add_expense(amount, str(expense_date), category, note)
        st.success("✅ Expense added successfully!")

# ---------------- View Expenses -----------------
elif choice == "View Expenses":
    st.header(" All Expenses")
    rows = db.get_expenses()
    if rows:
        df = pd.DataFrame(rows, columns=["id", "amount", "date", "category", "note"])
        df["date"] = pd.to_datetime(df["date"])

        # --- Filters in main page ---
        st.subheader(" Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date", df["date"].min().date())
        with col2:
            end_date = st.date_input("End Date", df["date"].max().date())
        with col3:
            categories = ["All"] + df["category"].unique().tolist()
            selected_cat = st.selectbox("Category", categories)

        # Apply filters
        mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
        if selected_cat != "All":
            mask &= df["category"] == selected_cat
        filtered_df = df[mask]

        st.write(f"Showing {len(filtered_df)} expenses")
        st.dataframe(filtered_df.style.applymap(highlight_large, subset=["amount"]))

        # Export CSV
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(" Download CSV", csv, "expenses.csv", "text/csv")

        # Update/Delete Section
        with st.expander(" Update or  Delete"):
            exp_id = st.number_input("Expense ID", min_value=1, step=1)
            if st.button("Delete Expense"):
                db.delete_expense(exp_id)
                st.warning(f"Deleted expense {exp_id}")
            if st.button("Update Expense"):
                new_amt = st.number_input("New Amount", min_value=0.0, format="%.2f", key="u_amt")
                new_date = st.date_input("New Date", date.today(), key="u_date")
                new_cat = st.text_input("New Category", "other")
                new_note = st.text_input("New Note", "")
                db.update_expense(exp_id, new_amt, str(new_date), new_cat, new_note)
                st.success("✅ Expense updated!")
    else:
        st.info("No expenses yet. Add one!")

# ---------------- Summary -----------------
elif choice == "Summary":
    st.header(" Expense Summary")
    rows = db.get_expenses()
    if rows:
        df = pd.DataFrame(rows, columns=["id", "amount", "date", "category", "note"])
        df["date"] = pd.to_datetime(df["date"])

        # --- Filters in main page ---
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date", df["date"].min().date(), key="sum_start")
        with col2:
            end_date = st.date_input("End Date", df["date"].max().date(), key="sum_end")
        with col3:
            categories = ["All"] + df["category"].unique().tolist()
            selected_cat = st.selectbox("Category", categories, key="sum_cat")

        # Apply filters
        mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
        if selected_cat != "All":
            mask &= df["category"] == selected_cat
        filtered_df = df[mask]

        # Metrics Cards
        total = round(filtered_df["amount"].sum(), 2)
        top_category = get_top_category(filtered_df)
        highest_expense = get_highest_expense(filtered_df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"${total}")
        col2.metric(" Top Category", top_category)
        col3.metric(" Highest Expense", f"${highest_expense}")

        # Expenses by Category
        st.subheader("By Category")
        if not filtered_df.empty:
            df_cat = filtered_df.groupby("category")["amount"].sum().reset_index()
            fig = px.bar(df_cat, x="category", y="amount", text="amount", color="amount",
                         color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet.")

        # Expenses by Month
        st.subheader("By Month")
        if not filtered_df.empty:
            df_month = filtered_df.copy()
            df_month["month"] = df_month["date"].dt.to_period("M").astype(str)
            df_month = df_month.groupby("month")["amount"].sum().reset_index()
            fig2 = px.line(df_month, x="month", y="amount", markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data yet.")

        # Top 5 Expenses
        st.subheader("Top 5 Expenses")
        if not filtered_df.empty:
            top5 = filtered_df.nlargest(5, "amount")
            fig3 = px.bar(top5, x="note", y="amount", text="amount", color="amount",
                          color_continuous_scale="Reds")
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No expenses yet. Add one!")


