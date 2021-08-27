import streamlit as st

def run_measureProfit():
    st.header("Measure Profit")
    capital = st.number_input("Capital: ", 0.0, value=0.0, key=0)
    fPrice = st.number_input("Buy Price: ", 0.0, value=0.0, key=1)
    sPrice = st.number_input("Target Price: ", 0.0, value=0.0, key=2)

    c1, c2 = st.beta_columns([1, 1])
    SLPercent = [1.5, 2]
    with c1:
        st.success("Stop loss (Short)")
        for x in SLPercent:
            value = x / 100 * capital
            SLPrice = fPrice * x / 100
            st.write(str(x) + "% = $" + str("{:.3f}".format(fPrice + SLPrice)) + " (Risk: $" + str(
                "{:.2f}".format(value)) + ")")

    with c2:
        st.success("Stop loss (Long)")
        for x in SLPercent:
            value = x / 100 * capital
            SLPrice = fPrice * x / 100
            st.write(str(x) + "% = $" + str("{:.3f}".format(fPrice - SLPrice)) + " (Risk: $" + str(
                "{:.2f}".format(value)) + ")")

    quotient = fPrice / sPrice
    percentage = (1 - quotient) * 100
    profit = (percentage / 100) * capital
    st.info("__Rewards__")
    fees = profit * 0.001
    totalprofit = profit - fees

    st.write("__Reward Percentage__: " + str("{:.2f}".format(percentage)) + "%")
    st.write("__Profit / Loss__: $" + str("{:.2f}".format(profit)))
    st.write("__Less Fees (0.1%)__: $" + str("{:.2f}".format(fees)))
    st.write("__Total Profit__: $" + str("{:.2f}".format(totalprofit)))