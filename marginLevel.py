import streamlit as st

def run_marginLevel():
    st.header("Margin Level")

    c1, c2 = st.columns([1, 1])
    with c1:
        pricePerCoin = st.number_input("Coin Price: ", 0.0, value=0.0, key=3)
    with c2:
        totalQuantity = st.number_input("Total Coin: ", 0.0, value=0.0, key=4)

    totalAsset = pricePerCoin * totalQuantity
    st.info("Assets: " + str("{:.2f}".format(totalAsset)))

    st.success("Margin Level = Total Asset Value / (Total Borrowed + Total Accrued Interest)")
    totalAssetValue = st.number_input("Total Asset: ", 0.0, value=0.0, key=0)

    c3, c4 = st.columns([1, 1])
    with c3:
        totalBorrowed = st.number_input("Total Borrowed: ", 0.0, value=0.0, key=1)
    with c4:
        totalAccruedInterest = st.number_input("Total Accrued Interest: ", 0.0, value=0.0, key=2)

    marginLevel = totalAssetValue / (totalBorrowed + totalAccruedInterest)
    st.info("Margin Level: " + str("{:.2f}".format(marginLevel)))

    if marginLevel < 1.1:
        st.warning("High risk")
        st.warning("Your assets will be automatically liquidated, meaning that Binance will sell your funds at market price to repay the loan.")
    elif marginLevel < 1.3:
        st.warning("Increase your collateral (by depositing more funds) or reduce your loan (by repaying what you’ve borrowed).")
    elif marginLevel < 1.5:
        st.warning("Low Risk")
    else:
        st.warning("Safe")

