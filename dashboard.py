import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Insights Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    return df

df = load_data()

# -------------------------
# CLEANING
# -------------------------

# Remove duplicate headers
df = df[df["Order Date"] != "Order Date"]

# Convert types
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")

# Drop nulls
df.dropna(inplace=True)

# Create Sales column
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

# Convert Order Date
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df = df.dropna(subset=["Order Date"])

# Extract useful features
df["Month"] = df["Order Date"].dt.month
df["Hour"] = df["Order Date"].dt.hour

# Extract City from address
df["City"] = df["Purchase Address"].apply(lambda x: x.split(",")[1])

# -------------------------
# SIDEBAR FILTER
# -------------------------
st.sidebar.header("Filters")

city = st.sidebar.selectbox(
    "Select City", ["All"] + sorted(df["City"].unique())
)

filtered_df = df.copy()

if city != "All":
    filtered_df = filtered_df[filtered_df["City"] == city]

# -------------------------
# KPI METRICS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Orders", len(filtered_df))
col3.metric("Avg Order Value", f"{filtered_df['Sales'].mean():.2f}")

# -------------------------
# CHARTS
# -------------------------

# 1️⃣ Sales by Product (Top 10)
st.subheader("📦 Top 10 Products by Sales")

product_sales = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(product_sales, x="Product", y="Sales", color="Product")
st.plotly_chart(fig, use_container_width=True)

# 2️⃣ Monthly Sales Trend
st.subheader("📅 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(monthly_sales, x="Month", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

# 3️⃣ Sales by City
st.subheader("🌍 Sales by City")

city_sales = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(city_sales, x="City", y="Sales", color="City")
st.plotly_chart(fig, use_container_width=True)

# 4️⃣ Orders by Hour (Peak time)
st.subheader("⏰ Orders by Hour")

hourly_orders = (
    filtered_df.groupby("Hour")["Quantity Ordered"]
    .count()
    .reset_index()
)

fig = px.line(hourly_orders, x="Hour", y="Quantity Ordered", markers=True)
st.plotly_chart(fig, use_container_width=True)

# 5️⃣ Profit-style Insight (Sales Distribution)
st.subheader("💰 Sales Distribution")

fig = px.histogram(filtered_df, x="Sales")
st.plotly_chart(fig, use_container_width=True)