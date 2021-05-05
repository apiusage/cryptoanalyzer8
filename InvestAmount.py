import streamlit as st
from openpyxl import Workbook
from db import * 
import pandas as pd
import plotly.express as px
import datetime

def run_investAmount():
    try:
        coinListDF = pd.read_excel('data/Coin List.xlsx', engine='openpyxl')  
        coinListDF = coinListDF['Coins List'].values.tolist()

        today = datetime.date.today()
        coin_transaction_date = st.date_input('Date: ', today)
        website = st.selectbox("Where: ", ['Binance'])
        coinName = st.selectbox("Coin Name: ", coinListDF)

        col1, col2 = st.beta_columns(2)
        
        with col1:
            st.info("__Buy__")
            buyPrice = st.number_input("Price: ", 0.0, value=0.0, key=0)
            boughtUnits = st.number_input("Units: ", 0.0, value=0.0, key=0)
            totalCost = buyPrice * boughtUnits
        
        with col2:
            st.info("__Sell__")
            sellPrice = st.number_input("Price: ", 0.0, value=0.0, key=1)
            soldUnits = st.number_input("Units: ", 0.0, value=0.0, key=1)
            totalSales = sellPrice * soldUnits

        c1, c2 = st.beta_columns([1,3])
        with c1:
            list_of_coins = [i[0] for i in view_all_data()]
            selected_coin = st.selectbox("Select Coin: ", list_of_coins)


        #if st.button('Add'):
       #     add_data(coinName, price, units, totalCost)
        #    st.success("Added {}".format(coinName))        
        
        #result = view_all_data()
        #df = pd.DataFrame(result, columns=['Coin Name', 'Per Coin Cost', 'Total Coins Qty', 'Total Cost'])
        #st.dataframe(df)

        #fig = px.pie(df, values = 'Total Coins Qty', names='Coin Name', title='Coins Distribution')
        #st.plotly_chart(fig, use_container_width=True)

    except:
        pass


    # amount to invest when drop
    # amount keep for interest

    #totalCoins = st.number_input("Enter Total Coins:", 0.0, value=0.0)
    #percentage = st.slider('Percentage', 0, 100, 50)

    #numOfCoin = totalCoins * (percentage/100)
    #st.info("Total coins: " + str("{:.2f}".format(numOfCoin)))


def sum_digits(n):
    n = int(n)
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s