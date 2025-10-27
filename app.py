import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import os

# get the absolute path of the current file (first.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")


###################################### Functions Part ######################################

# moved above main so it is defined before any call -> solves NameError
def create_kpi(mode, value, text, prefix="", suffix="", decimals=2, color="#1f77b4"):

    try:
        numeric_value = float(value)
        if pd.isna(numeric_value):
            numeric_value = 0.0
    except Exception:
        numeric_value = 0.0

    formatted_value = f"{prefix}{numeric_value:,.{decimals}f}{suffix}"

    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 10px;
            transition: transform 0.2s ease;
        "
        onmouseover="this.style.transform='scale(1.03)';"
        onmouseout="this.style.transform='scale(1)';">
            <div style="font-size: 34px; font-weight: bold; color: {color};">{formatted_value}</div>
            <div style="font-size: 14px; color: #444; margin-top: 5px;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

###################################### Main ######################################
def main():
    # Page config
    st.set_page_config(page_title="Brazilian Orders Story", page_icon="🇧🇷", layout="wide")
    ##########################################################

    # Sidebar navigation (story sections)
    section = st.sidebar.radio("Go to", (
        "Overview",
        "Revenue",
        "Order Level",
        "Delivery",
        "Customer Behavior",
        "Payment",
        "Time Series"
    ))

    # Header (Story title with short intro)
    st.markdown(
        "<div style='display:flex; align-items:center; gap:12px;'>"
        "<div style='font-size:42px;'>🇧🇷</div>"
        "<div><h1 style='margin:0;'>Brazilian Orders Story</h1>"
        "<p style='color:#555; margin:0;'>A quick interactive story that shows how orders, payments and delivery behave.</p></div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    ################################## Loading and standardize data ###########################

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'Data')

    sellers = pd.read_csv(os.path.join(DATA_DIR, 'vw_sellers_cleaned_sheet.csv'))
    customers = pd.read_csv(os.path.join(DATA_DIR, 'vw_customer_cleaned_sheet.csv'))
    orders = pd.read_csv(os.path.join(DATA_DIR, 'vw_order_cleaned_sheet.csv'))
    order_items = pd.read_csv(os.path.join(DATA_DIR, 'vw_order_items_cleaned_sheet.csv'))
    order_payment = pd.read_csv(os.path.join(DATA_DIR, 'vw_order_payment_cleaned_sheet.csv'))
    order_review = pd.read_csv(os.path.join(DATA_DIR, 'vw_order_review_cleaned_sheet.csv'))
    products = pd.read_csv(os.path.join(DATA_DIR, 'vw_product_cleaned_sheet.csv'))

    sellers.rename(columns={'Seller_Zip': 'seller_zip'}, inplace=True)

    orders.rename(columns={
        'Order_ID': 'order_id',
        'Customer_ID': 'customer_id',
        'Order_Status': 'order_status',
        'Order_Purchase_Timestamp': 'order_purchase_timestamp',
        'Order_Approved_At': 'order_approved_at',
        'Order_Delivered_Customer_Date': 'order_delivered_customer_date',
        'Order_Estimated_Delivery_Date': 'order_estimated_delivery_date'
    }, inplace=True)

    if 'Unnamed: 7' in order_review.columns:
        order_review.drop('Unnamed: 7', axis=1, inplace=True)

    products.rename(columns={
        'Product_ID': 'product_id',
        'Product_Category_Name': 'product_category_name',
        'Product_Category_Name_English': 'product_category_name_english',
        'product_photos_qty': 'product_photos_qty',
        'product_weight_g': 'product_weight_g',
        'Product_Length_CM': 'product_length_cm',
        'Product_Height_CM': 'product_height_cm',

        'Product_Width_CM': 'product_width_cm'
    }, inplace=True)

    pd.options.display.float_format = '{:,.0f}'.format

    ############################ Prepare Common Tables / KPIs #############################
    # Create a new column total_price
    order_items['total_price'] = order_items['price'] + order_items['freight_value']

    # Create a new table 'product_order_items' contains: product table and order_item table
    product_order_items = products.merge(order_items, on='product_id', how='inner')

    # Common KPIs used in multiple sections
    total_revenue = order_items['total_price'].sum()
    Avg_Total_Cost = order_items['total_price'].mean() if not order_items['total_price'].empty else 0
    Avg_Freight_Cost = order_items['freight_value'].mean() if 'freight_value' in order_items.columns else 0
    Frieght_cost_per_total = (Avg_Freight_Cost / Avg_Total_Cost) * 100 if Avg_Total_Cost != 0 else 0

    # Ensure datetime columns
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'], errors='coerce')
    orders['delivery_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    Average_delivery_time = orders['delivery_days'].median()

    customer_repeated_rate = (customers['customer_unique_id'].value_counts() > 1).mean() * 100
    payment_installments_avg = order_payment['payment_installments'].mean() if 'payment_installments' in order_payment.columns else 0

    ############################# OVERVIEW SECTION (KPIs) #############################
    if section == "Overview":
        st.markdown("### Overview — Highlights")
        st.write("A quick snapshot of the most important metrics. (This is the introduction to the story.)")

        # KPIs Row 1
        k1, k2, k3 = st.columns(3)
        with k1:
            create_kpi(mode='number', value=total_revenue, text='Total Revenue', prefix="$", decimals=0)
        with k2:
            create_kpi(mode='number', value=Frieght_cost_per_total, text='Freight Cost % of Total Orders', suffix="%", decimals=2)
        with k3:
            create_kpi(mode='number', value=Average_delivery_time, text='Average Delivery Time (days)', decimals=1)

        # KPIs Row 2
        k4, k5, k6 = st.columns(3)
        with k4:
            create_kpi(mode='number', value=customer_repeated_rate, text='Customer Repeated Rate', suffix="%", decimals=2)
        with k5:
            create_kpi(mode='number', value=payment_installments_avg, text='Avg Payment Installments', decimals=2)
        with k6:
            # Top payment value quick KPI
            order_payment_by_type = order_payment.groupby('payment_type')['payment_value'].sum().reset_index() if 'payment_value' in order_payment.columns else pd.DataFrame()
            order_payment_type_desc = order_payment_by_type.sort_values(by='payment_value', ascending=False) if not order_payment_by_type.empty else pd.DataFrame()
            top_payment_value = order_payment_type_desc['payment_value'].iloc[0] if not order_payment_type_desc.empty else 0
            create_kpi(mode='number', value=top_payment_value, text='Top Payment Value', prefix="$", decimals=0)

        st.markdown("---")
        st.markdown("**Quick insight:** The KPIs above are the headline of our story — keep scrolling to see the evidence that supports them.")

    ############################# REVENUE SECTION #############################


    if section == "Revenue":
        st.markdown("### Revenue — Where does money come from?")
        st.write("Top 10 product categories generate the highest revenue")

        # Create a new table 'product_order_items' contains: product table and order_item table
        top_ten_products = product_order_items.groupby('product_category_name_english')['total_price'].sum().sort_values(ascending=False).reset_index().head(10)
        st.write(top_ten_products)

        # Visualize the top 10 products
        fig1 = px.bar(
            top_ten_products,
            x='product_category_name_english',
            y='total_price',
            text='total_price',
            title='Top 10 Product Categories by Total Sales'
        )

        fig1.update_traces(
            texttemplate='%{text:.2s}',
            textposition='outside'
        )

        fig1.update_layout(
            xaxis_title='Product Category',
            yaxis_title='Total Sales',
            xaxis_tickangle=-45,
            showlegend=False,
            plot_bgcolor='white',
            width=900,
            height=500
        )

        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("**Insight:** A few categories contribute most revenue — consider focusing marketing or inventory on them.")

    ############################# ORDER LEVEL SECTION #############################


    if section == "Order Level":
        st.markdown("### Order-level Analysis — freight impact & distribution")
        st.write("Order summary table to show the impact of freight cost over final order value")

        # Creating a new table called 'orders_and_items' contains: orders table, and order_items table
        orders_and_items = pd.merge(orders, order_items, on='order_id')

        # order summary
        # contains: total price, freight value, final order summary
        order_summary = orders_and_items.groupby('order_id').agg(
            Total_Price=('total_price', 'sum'),
            freight_value=('freight_value', 'sum')
        )
        st.write(order_summary.head())

        # The average freight cost compared to total order value
        Avg_Total_Cost = order_items['total_price'].mean()
        Avg_Freight_Cost = order_items['freight_value'].mean()
        Frieght_cost_per_total = (Avg_Freight_Cost / Avg_Total_Cost) * 100 if Avg_Total_Cost != 0 else 0

        # Visualize the average freight cost compared to total order value
        create_kpi(mode='number', value=Frieght_cost_per_total, text='Freight Cost percentage of Total Orders', suffix="%", decimals=2)

        st.markdown("**Insight:** If freight is a large % of order value, consider negotiating shipping or adjusting pricing.")

    ############################# DELIVERY SECTION #############################


    if section == "Delivery":
        st.markdown("### Delivery Time Analysis — speed matters")
        # st.write("First ensure that the columns of dates are date datatype")

        # First ensure that the columns of dates are date datatype (already done above)
        # Then calculate the delivery days
        # orders['delivery_days'] computed above
        Average_delivery_time = orders['delivery_days'].median()

        # Visualize KPI2 : Average Delivery Time
        create_kpi(mode='number', value=Average_delivery_time, text='Average Delivery Time (days)', decimals=1)

        st.markdown("Now we want to know if there are outliers or not ?")
        # Visualize outliers (Plotly box)
        fig5 = px.box(
            orders,
            y='delivery_days',
            title='Delivery Days Distribution',
            points=False,
            color_discrete_sequence=['skyblue']
        )

        fig5.update_layout(
            yaxis_title='Days',
            template='plotly_white',
            width=900,
            height=450
        )

        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("Top 10 cities with the longest average delivery time")

        # Creating a new table called 'orders_and_customers' contains: orders table, and customers table
        orders_and_customers = orders.merge(customers, on='customer_id', how='inner')
        deliver_days_state = orders_and_customers[['delivery_days', 'customer_state']].sort_values(by='delivery_days', ascending=False).head(10)
        st.write('Delivery Days for each state')
        st.write(deliver_days_state)

        fig6 = px.bar(
            deliver_days_state,
            x='customer_state',
            y='delivery_days',
            title='Top 10 Cities with Longest Average Delivery Time',
            color='delivery_days',
            color_continuous_scale=['#1f77b4', '#2ca02c']
        )

        fig6.update_layout(
            xaxis_title='City',
            yaxis_title='Delivery Days',
            template='plotly_white',
            width=900,
            height=450
        )

        st.plotly_chart(fig6, use_container_width=True)

        st.markdown("**Insight:** Long delivery in specific cities suggests focusing logistics improvements regionally.")

    ############################# CUSTOMER BEHAVIOR SECTION #############################


    if section == "Customer Behavior":
        st.markdown("### Customer Behavior Metrics")
        st.write("Are customers repeat buying from us ?")
        customer_repeated_rate = (customers['customer_unique_id'].value_counts()>1).mean()
        create_kpi(mode='number', value=customer_repeated_rate*100, text='Customer Repeated Rate', suffix="%", decimals=2)

        # Review score distribution
        st.write("Review score distribution")
        fig7 = px.histogram(
            order_review,
            x='review_score',
            nbins=5,
            title='Distribution of Review Scores (1–5 Stars)',
            color_discrete_sequence=['#4C72B0']
        )
        fig7.update_layout(
            xaxis_title='Review Score',
            yaxis_title='Number of Reviews',
            bargap=0.1,
            width=700,
            height=450
        )
        st.plotly_chart(fig7, use_container_width=True)

        # Percentage of review score
        review_counts = order_review['review_score'].value_counts().sort_index()
        fig8 = px.pie(
            names=review_counts.index,
            values=review_counts.values,
            title='Review Score Distribution (in %)',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig8.update_traces(textinfo='percent+label')
        fig8.update_layout(width=700, height=450)
        st.plotly_chart(fig8, use_container_width=True)

        st.markdown("**Insight:** Monitor low-score segments and follow up with customers to improve retention.")

    ############################# PAYMENT SECTION #############################


    if section == "Payment":
        st.markdown("### Payment Summary")
        # Payment summary and visualizations
        order_payment_by_type = order_payment['payment_value'].groupby(order_payment['payment_type']).sum().reset_index()
        order_payment_type_desc = order_payment_by_type.sort_values(by='payment_value', ascending=False)

        # Visualize the total payment value
        fig_mat, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(order_payment_type_desc['payment_type'], order_payment_type_desc['payment_value'], color='skyblue')
        ax.set_xticklabels(order_payment_type_desc['payment_type'], rotation=45)
        ax.set_ylabel('Total Payment Value')
        ax.set_title('Total Payment Value by Payment Type')

        for i, v in enumerate(order_payment_type_desc['payment_value'].values):
            ax.text(i, v + max(order_payment_type_desc['payment_value']) * 0.01, f"${v:,.2f}", ha='center')

        st.pyplot(fig_mat)

        # Top payment value
        top_payment = order_payment_type_desc.head(1)
        create_kpi(mode='number', value=top_payment['payment_value'].iloc[0] if not top_payment.empty else 0, text='Top Payment', prefix="$", decimals=0)

        # The average number of installments
        payment_installments_avg = order_payment['payment_installments'].mean() if 'payment_installments' in order_payment.columns else 0
        create_kpi(mode='number', value=payment_installments_avg, text='Payment Installments Average', decimals=2)

        # The average of orders per payment type
        payment_type_count = order_payment['order_id'].groupby(order_payment['payment_type']).count().reset_index()

        fig9 = px.bar(
            payment_type_count,
            x='payment_type',
            y='order_id',
            title='Number of Orders per Payment Type',
            color='order_id',
            color_continuous_scale=['#1f77b4', '#2ca02c']
        )

        fig9.update_layout(
            xaxis_title='Payment Type',
            yaxis_title='Number of Orders',
            template='plotly_white',
            width=900,
            height=450
        )

        st.plotly_chart(fig9, use_container_width=True)

        # Average payment distribution by payment type
        avg_payment = order_payment.groupby('payment_type')['payment_value'].mean().reset_index()

        fig10 = px.pie(
            avg_payment,
            names='payment_type',
            values='payment_value',
            title='Average Payment Distribution by Payment Type',
            color_discrete_sequence=px.colors.sequential.Greens,
            width=700,
            height=450
        )

        st.plotly_chart(fig10, use_container_width=True)

        st.markdown("**Insight:** Which payment types bring higher value? Are some risky or costly?")

    ############################# TIME SERIES SECTION #############################


    if section == "Time Series":
        st.markdown("### Time Series — trends over time")

        # The number of orders per month
        orders['purchase_month'] = orders['order_purchase_timestamp'].dt.month
        orders_per_month = orders['order_id'].groupby(orders['purchase_month']).count().reset_index()
        fig11 = px.line(
            orders_per_month,
            x='purchase_month',
            y='order_id',
            markers=True,
            title='Monthly Orders Trend',
        )

        fig11.update_traces(line=dict(color='royalblue', width=3))
        fig11.update_layout(
            xaxis_title='Month',
            yaxis_title='Number of Orders',
            template='plotly_white',
            width=900,
            height=450
        )

        st.plotly_chart(fig11, use_container_width=True)

        # Total revenue per year
        orders['purchase_year'] = orders['order_purchase_timestamp'].dt.year

        # create a new table called full_info contains order table and product_order_items
        full_info = orders.merge(product_order_items, on='order_id')
        yearly_revenue = full_info.groupby('purchase_year')['total_price'].sum().reset_index()

        fig12 = px.line(
            yearly_revenue,
            x='purchase_year',
            y='total_price',
            title='Yearly Total Revenue Trend',
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#0b3d91']
        )

        fig12.update_traces(marker=dict(size=8, color='#1f77b4', line=dict(width=2, color='#0b3d91')))
        fig12.update_layout(
            template='simple_white',
            xaxis_title='Year',
            yaxis_title='Total Revenue',
            title_x=0.5,
            title_font=dict(size=16),
            width=900,
            height=450
        )

        st.plotly_chart(fig12, use_container_width=True)

        st.markdown("**Insight:** Look for seasonal spikes and investigate drivers (campaigns, product launches, discounts).")

    # End of sections
    st.markdown("---")

if __name__ == "__main__":
    main()
