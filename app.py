import streamlit as st
import pandas as pd

# ✅ Function to load and clean data
@st.cache_data
def load_data(file_path):
    # Load CSV
    df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

    # ✅ Standardize column names (remove leading/trailing spaces)
    df.columns = df.columns.str.strip()

    # ✅ Check if "Order Date" exists
    if "Order Date" not in df.columns:
        st.error("❌ 'Order Date' column not found in dataset!")
        st.stop()

    # ✅ Trim spaces in "Order Date" values
    df["Order Date"] = df["Order Date"].astype(str).str.strip()

    # ✅ Convert to datetime safely
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", infer_datetime_format=True)

    # ✅ Find and log invalid dates
    invalid_dates = df[df["Order Date"].isna()]
    if not invalid_dates.empty:
        st.warning(f"⚠️ Found {len(invalid_dates)} invalid date entries!")
        st.write(invalid_dates[["Order Date"]])

    # ✅ Remove invalid dates
    df.dropna(subset=["Order Date"], inplace=True)
    df.columns = df.columns.str.strip()  # Remove column name spaces
    df = df[df["Order Date"].notnull()]  # Drop empty date rows
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")  # Convert & ignore errors
    df = df.dropna(subset=["Order Date"])  # Remove rows where conversion failed


    return df

# ✅ Streamlit UI
st.title("📊 Sales Insights EDA")

# Hardcoded file path (update this to the location of your file)
file_path = 'F:\\SalesInsightEDA\\all_data.csv'

# Load the data directly
df = load_data(file_path)

# ✅ Show cleaned dataset
st.write("### 🔍 Cleaned Data Preview")
st.dataframe(df.head())

# ✅ Sidebar Filters
st.sidebar.header("🔍 Filters")

# ✅ Check if "Product" column exists
if "Product" in df.columns:
    selected_product = st.sidebar.selectbox("Select Product", df["Product"].unique())
    df_filtered = df[df["Product"] == selected_product]
else:
    st.sidebar.warning("⚠️ 'Product' column not found!")
    df_filtered = df

# ✅ Display filtered data
st.write(f"### 📌 Data for {selected_product}")
st.dataframe(df_filtered)

# ✅ Compute & Display Sales Summary
if "Quantity Ordered" in df.columns and "Price Each" in df.columns:
    df_filtered["Quantity Ordered"] = pd.to_numeric(df_filtered["Quantity Ordered"], errors="coerce")
    df_filtered["Price Each"] = pd.to_numeric(df_filtered["Price Each"], errors="coerce")
    df_filtered["Total Sales"] = df_filtered["Quantity Ordered"] * df_filtered["Price Each"]
    st.write(f"### 💰 Total Sales for {selected_product}: **₹{df_filtered['Total Sales'].sum():,.2f}**")
else:
    st.warning("⚠️ Sales calculation columns not found!")
