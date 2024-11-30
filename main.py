import streamlit as st
import pandas as pd
import openai_helper  # Your helper file

# Default empty dataframe
financial_data_df = pd.DataFrame({
    "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
    "Value": ["", "", "", "", ""]
})

# Layout
st.title("Financial Data Entity Extraction Tool")
option = st.radio(
    "Choose an option to fetch financial data:",
    ("Extract from News Article", "Fetch by Company Name")
)

if option == "Extract from News Article":
    news_article = st.text_area("Paste your financial news article or data here", height=300)
    if st.button("Extract Entity from Article"):
        financial_data_df = openai_helper.extract_financial_data(news_article)

elif option == "Fetch by Company Name":
    company_name = st.text_input("Enter the company name or stock ticker (e.g., TSLA for Tesla):")
    if st.button("Fetch Financial Data"):
        financial_data_df = openai_helper.fetch_company_financial_data(company_name)

# Display Dataframe
st.dataframe(
    financial_data_df,
    column_config={
        "Measure": st.column_config.Column(width=150),
        "Value": st.column_config.Column(width=150)
    },
    hide_index=True
)
