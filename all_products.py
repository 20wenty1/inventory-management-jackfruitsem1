import sqlite3
import streamlit as st
import pandas as pd

st.title("All Products")

# ---------- SEARCH BAR ----------
search_query = st.text_input("Product Name", "")

col1, col2 = st.columns(2)

# Connect to DB
def load_data(query=None):
    con = sqlite3.connect("supermarket.db")
    cur = con.cursor()

    if query:
        cur.execute(
            "SELECT id, name, price, stock FROM products WHERE name LIKE ?",
            ('%' + query + '%',)
        )
    else:
        cur.execute("SELECT id, name, price, stock FROM products")

    rows = cur.fetchall()
    con.close()

    df = pd.DataFrame(rows, columns=["ID", "Name", "Price", "Stock"])
    return df

# Default empty dataframe shown
df = pd.DataFrame(columns=["ID", "Name", "Price", "Stock"])

# SEARCH BUTTON
with col1:
    if st.button("Search"):
        df = load_data(search_query)

# SHOW ALL BUTTON
with col2:
    if st.button("Show All"):
        df = load_data()

# DISPLAY TABLE
if not df.empty:
    st.subheader("Results")
    st.dataframe(df, use_container_width=True)