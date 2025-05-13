
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Simulated stock data
items = ['Bread', 'Milk', 'Rice', 'Soap', 'Sugar', 'Tea', 'Salt', 'Oil']
categories = ['Food', 'Beverage', 'Grain', 'Toiletries', 'Sweetener', 'Beverage', 'Spices', 'Cooking']

np.random.seed(42)
stock_data = pd.DataFrame({
    'Item Name': items,
    'Category': categories,
    'Quantity': np.random.randint(5, 100, size=len(items)),
    'Unit Price (R)': np.round(np.random.uniform(10, 50, size=len(items)), 2),
    'Last Restocked': pd.to_datetime("2024-05-01") + pd.to_timedelta(np.random.randint(1, 10, size=len(items)), unit="D"),
    'Daily Sales Rate': np.round(np.random.uniform(1, 10, size=len(items)), 1)
})

stock_data['Predicted Days Left'] = (stock_data['Quantity'] / stock_data['Daily Sales Rate']).round(1)
stock_data['Restock Alert'] = stock_data['Predicted Days Left'] < 7

# Streamlit UI
st.title("📦 Local Business Stock Dashboard")

st.header("Current Inventory")
st.dataframe(stock_data.style.apply(lambda row: ['background-color: red' if row.Restock_Alert else '' for _ in row], axis=1))

st.header("📉 Low Stock Alerts")
low_stock = stock_data[stock_data['Restock Alert']]
if not low_stock.empty:
    st.warning("The following items are running low and need restocking soon:")
    st.table(low_stock[['Item Name', 'Quantity', 'Predicted Days Left']])
else:
    st.success("All items are sufficiently stocked.")

st.header("📊 Inventory Overview")
st.bar_chart(stock_data.set_index('Item Name')['Quantity'])

st.header("🔄 Restock Simulation")
item_to_restock = st.selectbox("Select an item to simulate restock:", stock_data['Item Name'])
additional_stock = st.slider("How many units to add?", min_value=1, max_value=100, value=20)
if st.button("Simulate Restock"):
    idx = stock_data[stock_data['Item Name'] == item_to_restock].index[0]
    stock_data.at[idx, 'Quantity'] += additional_stock
    stock_data.at[idx, 'Last Restocked'] = datetime.now()
    stock_data.at[idx, 'Predicted Days Left'] = (stock_data.at[idx, 'Quantity'] / stock_data.at[idx, 'Daily Sales Rate']).round(1)
    stock_data.at[idx, 'Restock Alert'] = stock_data.at[idx, 'Predicted Days Left'] < 7
    st.success(f"Restocked {additional_stock} units of {item_to_restock}.")
    st.dataframe(stock_data)
