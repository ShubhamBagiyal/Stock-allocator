import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Stock Portfolio Allocator")

total_investment = st.number_input(
    "Enter Total Investment Amount (₹)",
    min_value=1000,
    value=100000
)

num_stocks = st.slider(
    "How many stocks?",
    min_value=2,
    max_value=10,
    value=5
)

stocks = []
for i in range(num_stocks):
    ticker = st.text_input(
        f"Enter Stock {i+1} Ticker (e.g. TCS.NS)",
        key=f"stock_{i}"
    )
    stocks.append(ticker)

if st.button("🔍 Calculate Allocation"):
    money_per_stock = total_investment / num_stocks
    results = []
    prices = {}  # store prices separately for reuse later

    for ticker in stocks:
        if ticker == "":
            st.warning("Please fill in all stock tickers!")
            st.stop()
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prices[ticker.upper()] = price  # save price for later
            shares = int(money_per_stock / price)
            spent = shares * price
            leftover = money_per_stock - spent
            results.append({
                "Stock": ticker.upper(),
                "Live Price (₹)": round(price, 2),
                "Shares to Buy": shares,
                "Amount Spent (₹)": round(spent, 2),
                "Leftover (₹)": round(leftover, 2)
            })
        except Exception as e:
            st.error(f"Could not fetch data for {ticker}. Check the ticker symbol!")
            st.stop()

    df = pd.DataFrame(results)

    # --- Unspent money reinvestment ---
    total_leftover = total_investment - df["Amount Spent (₹)"].sum()

    # find the cheapest stock
    cheapest_stock = min(prices, key=prices.get)
    cheapest_price = prices[cheapest_stock]

    if total_leftover >= cheapest_price:
        extra_shares = int(total_leftover / cheapest_price)
        extra_spent = extra_shares * cheapest_price
        total_leftover = total_leftover - extra_spent

        # update that stock's row in the dataframe
        idx = df[df["Stock"] == cheapest_stock].index[0]
        df.at[idx, "Shares to Buy"] += extra_shares
        df.at[idx, "Amount Spent (₹)"] += round(extra_spent, 2)
        df.at[idx, "Leftover (₹)"] = round(
            df.at[idx, "Leftover (₹)"] - extra_spent, 2
        )
        st.success(f"✅ Allocation Complete! Bought {extra_shares} extra share(s) of {cheapest_stock} with unspent cash.")
    else:
        st.success("✅ Allocation Complete!")

    st.subheader("Results Table")
    st.dataframe(df)

    st.subheader("Portfolio Allocation Chart")
    fig, ax = plt.subplots()
    ax.pie(
        df["Amount Spent (₹)"],
        labels=df["Stock"],
        autopct='%1.1f%%'
    )
    ax.set_title("Where your money goes")
    st.pyplot(fig)

    total_spent = df["Amount Spent (₹)"].sum()
    st.info(f"💰 Total Spent: ₹{round(total_spent, 2)} | Remaining Unspent: ₹{round(total_leftover, 2)}")