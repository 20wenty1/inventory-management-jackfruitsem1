import sqlite3
import streamlit as st
import pandas as pd

# ---------------- STYLE ----------------
st.markdown("""
<style>
.box {
    border: 2px solid #1b4f72;
    padding: 15px;
    border-radius: 5px;
    background-color: #f0f6ff;
}
.title-bar {
    background-color: #1b4f72;
    color: white;
    padding: 6px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
    border-radius: 3px;
}
.btn {
    background-color: #1b4f72 !important;
    color: white !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown('<div class="box">', unsafe_allow_html=True)
st.markdown('<div class="title-bar">All Products</div>', unsafe_allow_html=True)

product_name = st.text_input("Product Name")

col1, col2 = st.columns(2)

def fetch(query=None):
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

    return pd.DataFrame(rows, columns=["ID", "Name", "Price", "Quantity"])

df = pd.DataFrame()
with col1:
    if st.button("Search", help="Search for product", use_container_width=True):
        df = fetch(product_name)
if not df.empty:
    st.dataframe(df, use_container_width=True, height=300)

st.markdown('</div>', unsafe_allow_html=True)
