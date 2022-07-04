import streamlit as st
import streamlit.components.v1 as stc
from db import * 
from portfolio import *
from marginLevel import *
from measureProfit import *
from potentialCoinAnalyzer import *
from PIL import Image

img = Image.open("Logo.png").convert('RGB').save('Logo.jpeg')
PAGE_CONFIG = {"page_title": "Crypto Analyzer", "page_icon":img, "layout":"wide", "initial_sidebar_state": "expanded" }
st.set_page_config(**PAGE_CONFIG)

LOGO_BANNER = """
    <div style="background-color:#464e5f;padding:3px;border-radius:10px";>
    <h1 style="color:white;text-align:center;"> Crypto Analyzer </h1>
    </div>
    """

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    # try:
        stc.html(LOGO_BANNER)
        menu = ["Home", "Measure Profit", "Margin Level", "Trading View", "Portfolio", "About"]
        choice = st.sidebar.selectbox("Menu", menu)

        create_table()

        if choice == "Home":
            run_potentialCoin()

        if choice == "Margin Level":
            run_marginLevel()

        elif choice == "Trading View":
            run_tradingView()

        elif choice == "Measure Profit":
            run_measureProfit()

        elif choice == "Portfolio":
            run_portfolio()

        elif choice == "About":
            st.header("About")
            st.write("Crypto Analyzer")
            st.balloons()

    #except:
     #   pass

if __name__ == '__main__':
    main()



