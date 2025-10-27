**Brazilian Orders Analysis**

This project analyzes Brazilian e-commerce orders over 3 years. 
It provides insights into customer behavior, order patterns, product performance, and reviews using interactive visualizations.

- Features:
  - Cleaned and processed datasets for sellers, customers, orders, payments, reviews, and products.
  - Analysis of top products, customer repeat rate, delivery times, and reviews.
  - Built with Python, Pandas, Matplotlib, Plotly, and Streamlit.

- Dataset:
The project uses the following datasets (cleaned versions included in the Data folder):
  - vm_sellers_cleaned_sheet.csv – Seller information
  - vw_customer_cleaned_sheet.csv – Customer information
  - vw_order_cleaned_sheet.csv – Orders details
  - vw_order_items_cleaned_sheet.csv – Items per order
  - vw_order_payment_cleaned_sheet.csv – Payment information
  - vw_order_review_cleaned_sheet.csv – Customer reviews
  - vw_product_cleaned_sheet.csv – Products information

- How to Run Locally?

  Clone the repository:
  
  git clone https://github.com/habibaIbrahim276/Brazilian_Orders.git
  cd Brazilian_Orders
  
  
  Create a virtual environment and install dependencies:
  
  python -m venv .venv
  .venv\Scripts\activate   # Windows
  pip install -r requirements.txt
  
  
  Run the Streamlit app:
  
  streamlit run app.py
  
  
  Open the provided local URL in your browser to interact with the dashboard.
  
  Deployment

**The app is deployed online using Streamlit Cloud and can be accessed here**

https://habibaibrahim276-brazilian-orders-app-ersrxn.streamlit.app/

- License

  This project is open-source and available under the MIT License.
