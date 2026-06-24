import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Business Sales Analytics Dashboard",
    page_icon="",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(
    "Sample - Superstore copy.csv",
    encoding="latin1"
)

df['Order Date'] = pd.to_datetime(df['Order Date'])

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

selected_segments = st.sidebar.multiselect(
    "Select Segment",
    df['Segment'].unique(),
    default=df['Segment'].unique()
)

df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['Segment'].isin(selected_segments))
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Business Sales Performance Analytics Dashboard")

st.caption(
    "Future Interns | Data Science & Analytics Task 1"
)

st.markdown("---")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
avg_order_value = total_sales / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "Orders",
    f"{total_orders}"
)

col4.metric(
    "Avg Order Value",
    f"${avg_order_value:,.2f}"
)

st.markdown("---")

# --------------------------------------------------
# MONTHLY SALES TREND
# --------------------------------------------------

monthly_sales = (
    df.groupby(
        df['Order Date'].dt.to_period('M')
    )['Sales']
    .sum()
    .reset_index()
)

monthly_sales['Order Date'] = monthly_sales['Order Date'].astype(str)

fig1 = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    title='Monthly Revenue Trend',
    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------------------------
# REGION + CATEGORY
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    region_sales = (
        df.groupby('Region')['Sales']
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        title='Revenue by Region'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    category_sales = (
        df.groupby('Category')['Sales']
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names='Category',
        values='Sales',
        hole=0.5,
        title='Sales by Category'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# --------------------------------------------------
# PROFIT ANALYSIS
# --------------------------------------------------

profit_category = (
    df.groupby('Category')['Profit']
    .sum()
    .reset_index()
)

fig4 = px.bar(
    profit_category,
    x='Category',
    y='Profit',
    title='Profit by Category'
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

top_products = (
    df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x='Sales',
    y='Product Name',
    orientation='h',
    title='Top 10 Products by Revenue'
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.markdown("---")

st.subheader("Key Business Insights")

st.success("""
1.Technology category generates the highest sales and profit.

2.West region contributes the highest revenue.

3.South region shows the lowest sales performance.

4.Revenue demonstrates an overall growth trend over time.

5.Top-selling products contribute significantly to total business revenue.
""")

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(df.head(50))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Created by Sri Sakthi P | Future Interns Data Science & Analytics Project"
)