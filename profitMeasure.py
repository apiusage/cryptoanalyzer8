import streamlit as st
from db import * 

def run_profitMeasure():
    st.header("Measure Profit")

    capital = st.number_input("Capital: ", 0, value=0, key=0)
    value = st.slider('Coin Price Changes: ', 1.0, 1.5, (1.1, 1.3))
    
    quotient = value[0] / value[1] 
    percentage = (1-quotient) * 100
    profit = (percentage/100) * capital
    st.info("__Lowest:__" + " "  + str(value[0]) + "     " + "__Highest:__" + " " + str(value[1]))
    fees = profit * 0.1000
    totalprofit = profit - fees

    st.write("__Percentage__: " + str("{:.2f}".format(percentage)) + "%")
    st.write("__Profit__: $" + str("{:.2f}".format(profit)))
    st.write("__Less Fees (0.1%)__: $" + str("{:.2f}".format(fees)))
    st.write("__Total Profit__: $" + str("{:.2f}".format(totalprofit)))

