import streamlit as st
import streamlit.components.v1 as stc
from db import * 
from portfolio import *
from profitMeasure import *
from marginLevel import *
from PIL import Image

img = Image.open("Logo.png").convert('RGB').save('Logo.jpeg')
PAGE_CONFIG = {"page_title": "Crypto Analyzer", "page_icon":img, "layout":"centered", "initial_sidebar_state": "expanded" }
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
    except:
        pass


if __name__ == '__main__':
    main()