import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Title
st.set_page_config(page_title="Sales Insights Dashboard", layout="wide")

# Load Data
@st.cache_data  # Caching to improve performance
def load_data():
    df = pd.read_csv("all_data.csv")  # Replace with your dataset file name
    df["Order Date"] = pd.to_datetime(df["Order Date"])  # Ensure correct date format
    return df

df = load_data()

# Sidebar - User Inputs
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox("Select Product Category", df["Category"].unique())

# Filter Data
filtered_data = df[df["Category"] == selected_category]

# Dashboard Title
st.title("📊 Sales Insights Dashboard")
st.write("## Overview of Sales Data")
st.dataframe(df.head())  # Show raw data preview

# Key Metrics
st.write("## 📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
col2.metric("Total Orders", df.shape[0])
col3.metric("Total Profit", f"${df['Profit'].sum():,.2f}")

# Sales Trend Chart
st.write("## 📈 Sales Over Time")
fig, ax = plt.subplots(figsize=(10, 4))
df.groupby("Order Date")["Sales"].sum().plot(ax=ax, color="blue", marker="o")
ax.set_xlabel("Date")
ax.set_ylabel("Total Sales")
st.pyplot(fig)

# Category-wise Sales
st.write("## 📊 Sales by Category")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=df["Category"], y=df["Sales"], ax=ax, palette="coolwarm")
ax.set_xlabel("Category")
ax.set_ylabel("Total Sales")
st.pyplot(fig)

# Show Filtered Data
st.write(f"## 🔍 Sales Data for {selected_category}")
st.dataframe(filtered_data)

# Footer
st.markdown("---")
st.markdown("👩‍💻 **Developed by Satakshi**")

