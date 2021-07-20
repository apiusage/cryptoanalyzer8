import streamlit as st
import streamlit.components.v1 as stc
from db import * 
from portfolio import *
from marginLevel import *
from PIL import Image

img = Image.open("Logo.png").convert('RGB').save('Logo.jpeg')
PAGE_CONFIG = {"page_title": "Crypto Analyzer", "page_icon":img, "layout":"centered", "initial_sidebar_state": "collapsed" }
st.set_page_config(**PAGE_CONFIG)

LOGO_BANNER = """
    <div style="background-color:#464e5f;padding:3px;border-radius:10px";>
    <h1 style="color:white;text-align:center;"> Crypto Analyzer </h1>
    </div>
    """

def main():
    try:
        stc.html(LOGO_BANNER)
        menu = ["Home", "Margin Level", "Profit Measurement", "Portfolio", "About"]
        choice = st.sidebar.selectbox("Menu", menu)

        create_table()

        if choice == "Margin Level":
            run_marginLevel()

        elif choice == "Profit Measurement":
            run_profitMeasure()

        elif choice == "Portfolio":   
            run_portfolio() 

        elif choice == "About":
            st.header("About")
            st.write("Crypto Analyzer")
            st.balloons()

        st.header("Measure Profit")
        capital = st.number_input("Capital: ", 0, value=0, key=0)
        fPrice = st.number_input("Buy Price: ", 0.0, value=0.0, key=1)
        sPrice = st.number_input("Target Price: ", 0.0, value=0.0, key=2)

        c1, c2 = st.beta_columns([1, 1])
        with c1:
            st.success("Stop loss (Short)")
            SLPercent = [1.5, 2]
            for x in SLPercent:
                SLPrice = fPrice * x / 100
                st.write(str(x) + "% = $" + str("{:.2f}".format(fPrice + SLPrice)))

        with c2:
            st.success("Stop loss (Long)")
            for x in SLPercent:
                SLPrice = fPrice * x / 100
                st.write(str(x) + "% = $" + str("{:.2f}".format(fPrice - SLPrice)))

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
    except:
        pass

if __name__ == '__main__':
    main()