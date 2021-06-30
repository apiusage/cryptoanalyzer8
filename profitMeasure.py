import streamlit as st
from db import * 

def run_profitMeasure():
    st.header("Measure Profit")

    capital = st.number_input("Capital: ", 0, value=0, key=0)

    c1, c2 = st.beta_columns([1, 1])
    with c1:
        fPrice = st.number_input("1st Price: ", 0.0, value=0.0, key=1)
    with c2:
        sPrice = st.number_input("2nd Price: ", 0.0, value=0.0, key=2)

    quotient = fPrice / sPrice
    percentage = (1-quotient) * 100
    profit = (percentage/100) * capital
    st.info("__Lowest:__" + " "  + str(fPrice) + "     " + "__Highest:__" + " " + str(sPrice))
    fees = profit * 0.001
    totalprofit = profit - fees

    st.write("__Percentage__: " + str("{:.2f}".format(percentage)) + "%")
    st.write("__Profit__: $" + str("{:.2f}".format(profit)))
    st.write("__Less Fees (0.1%)__: $" + str("{:.2f}".format(fees)))
    st.write("__Total Profit__: $" + str("{:.2f}".format(totalprofit)))

