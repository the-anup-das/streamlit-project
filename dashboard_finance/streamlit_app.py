import yfinance as yf
import streamlit as st

st.write(
    """
    # Simple Stock Price App

    Shown are the stock **chosing price** and ***volume*** of Google!
    """
)

# define the ticker symbol
tickerSymbol = 'GOOGL'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='Id', start='2010-5-31', end='2022-7-31')

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)