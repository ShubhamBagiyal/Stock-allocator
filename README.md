# 📊 Stock Portfolio Allocator

A web app that distributes your investment amount across multiple NSE stocks using live market prices.

## Features
- Enter any investment amount
- Choose number of stocks (2–10)
- Fetches live stock prices from Yahoo Finance
- Calculates exact shares you can buy per stock
- Reinvests unspent cash into the cheapest stock automatically
- Shows results table + portfolio pie chart

## Tech Stack
- Python
- Streamlit
- yfinance
- Pandas
- Matplotlib

## How to Run Locally
pip install -r requirements.txt
streamlit run app.py

## Live Demo
[Live App](https://stock-allocator-firfrfexq86ubuosrvyqpb.streamlit.app/)
