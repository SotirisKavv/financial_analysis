import os
from openai import OpenAI
import streamlit as st
import yfinance as yf
import pandas as pd

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)



def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def get_summary(ticker_1, stock_data_1, ticker_2, stock_data_2):
    SYSTEM_MSG = """
                You are a financial assistant that will retrieve two tables of financial market data and will summarize 
                the comparative performance in text, in full detail with highlights for each stock and also a conclusion 
                with a markdown output. BE VERY STRICT ON YOUR OUTPUT
            """
    CONTENT_MSG = f"This is the {ticker_1} stock data : {stock_data_1}, this is {ticker_2} stock data: {stock_data_2}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": CONTENT_MSG}
        ] 
    )
    
    return response.choices[0].message.content

st.title("Financial Market Analysis")

st.sidebar.header("Options")
stock_ticker_1 = st.sidebar.text_input("Enter Stock Ticker", "AAPL").upper()
stock_ticker_2 = st.sidebar.text_input("Enter Stock Ticker", "GOOGL").upper()

side_cols = st.sidebar.columns(2)
with side_cols[0]:
    side_cols[0].subheader("Start Date")
    start_date = side_cols[0].date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    
with side_cols[1]:
    side_cols[1].subheader("End Date")
    end_date = side_cols[1].date_input("End Date", value=pd.to_datetime('2024-02-01'))

cols = st.columns(2)

with cols[0]:
    if stock_ticker_1:
        st_data_1 = get_stock_data(stock_ticker_1, start_date=str(start_date), end_date=str(end_date))
        st.subheader(f"Displaying Data for {stock_ticker_1}")
        tabs_1 = st.tabs(["Chart", "Analytics"])
        with tabs_1[0]:
            chart_type_1 = st.sidebar.selectbox(f"Select Chart Type for {stock_ticker_1}", ["Line", "Bar"], key="chart_1")
            if chart_type_1 == "Line":
                st.line_chart(st_data_1['Close'])
            elif chart_type_1 == "Bar":
                st.bar_chart(st_data_1['Close'])
        with tabs_1[1]:
            st.write(st_data_1)

with cols[1]:
    if stock_ticker_2:
        st_data_2 = get_stock_data(stock_ticker_2, start_date=str(start_date), end_date=str(end_date))
        st.subheader(f"Displaying Data for {stock_ticker_2}")
        tabs_2 = st.tabs(["Chart", "Analytics"])
        with tabs_2[0]:
            chart_type_2 = st.sidebar.selectbox(f"Select Chart Type for {stock_ticker_2}", ["Line", "Bar"], key="chart_2")
            if chart_type_2 == "Line":
                st.line_chart(st_data_2['Close'])
            elif chart_type_2 == "Bar":
                st.bar_chart(st_data_2['Close'])
        with tabs_2[1]:
            st.write(st_data_2)
    
if st.button("Comparative Performance") and stock_ticker_1 and stock_ticker_2:
    summary = get_summary(stock_ticker_1, st_data_1, stock_ticker_2, st_data_2)
    st.write(summary)