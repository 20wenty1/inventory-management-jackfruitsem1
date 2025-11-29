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
</style>
""", unsafe_allow_html=True)

# ---------------- CONTAINER ----------------
st.markdown('<div class="box">', unsafe_allow_html=True)
st.markdown('<div class="title-bar">All Products</div>', unsafe_allow_html=True)

# ---------------- SEARCH INPUT ----------------
product_name = st.text_input("Product Name")

col1, col2 = st.columns(2)

# ---------------- LOAD DATA ----------------
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


# --------- CUMULATIVE SEARCH RESULTS ---------
if "search_results" not in st.session_state:
    st.session_state.search_results = pd.DataFrame(columns=["ID", "Name", "Price", "Quantity"])

with col1:
    if st.button("Search"):
        new_result = fetch(product_name.strip())

        # Add new results below previous ones
        st.session_state.search_results = pd.concat(
            [st.session_state.search_results, new_result],
            ignore_index=True
        )

with col2:
    if st.button("Show All"):
        st.session_state.search_results = fetch()

# --------- DISPLAY TABLE ---------
if not st.session_state.search_results.empty:
    st.dataframe(st.session_state.search_results, use_container_width=True, height=350)


# CLOSE BOX
st.markdown('</div>', unsafe_allow_html=True)
