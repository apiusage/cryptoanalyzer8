import streamlit as st
from openpyxl import Workbook
from db import * 
import pandas as pd
import plotly.express as px
import datetime

def run_portfolio():
    try:
        viewAnalysis()
        buy_coin()
        sell_coin()
        delete_coin()
    except:
        pass

def viewAnalysis():
    try:
        result = view_all_data()
        df = pd.DataFrame(result)
        c1, c2 = st.beta_columns([1,3])
        with c1:
            list_of_coin = [i[2] for i in view_all_data()]
            selected_coin = st.selectbox("Select Coin: ", list_of_coin)

        with c2:
            coin_result = get_coin_by_name(selected_coin)
            coin_transaction_date = coin_result[0][0]
            exchange = coin_result[0][1]
            coinName = coin_result[0][2]
            buyPrice = coin_result[0][3]
            boughtUnits = coin_result[0][4]
            totalCost = coin_result[0][5]
            sellPrice = coin_result[0][6]
            soldUnits = coin_result[0][7]
            totalSales = coin_result[0][8]
            profit = coin_result[0][9]

            st.info("__Coin__: {}".format(coinName))
            st.markdown("__Date:__ {}".format(coin_transaction_date))
            st.markdown("__Exchange:__ {}".format(exchange))

            st.markdown("__Buy Price:__ {}".format("$" + buyPrice) + " " +
                        "__Sell Price:__ {}".format("$" + sellPrice))

            st.markdown("__Bought Units:__ {}".format(boughtUnits) + " " +
                        "__Sold Units:__ {}".format(soldUnits))
                        
            st.markdown("__Total Cost:__ {}".format("$" + totalCost) + " " +
                        "__Total Sales:__ {}".format("$" + totalSales))

            st.success("__Profit:__ {}".format("$" + profit))
            
            df = pd.DataFrame(result, columns=['Date', 'Exchange', 'Coin Name', 'Buy Price', 'Bought Units', 'Total Cost', 'Sell Price', 'Sold Units', 'Total Sales', 'Profit'])
            fig = px.pie(df, values = 'Bought Units', names='Coin Name', title='Coins Distribution')
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart
            fig2 = px.bar(df, x = 'Coin Name', y = 'Profit')
            st.plotly_chart(fig2, use_container_width=True)
    except:
        pass

def buy_coin(): 
    with st.beta_expander("Buy Coin"):
        coinListDF = pd.read_excel('data/Coin List.xlsx', engine='openpyxl')  
        coinListDF = coinListDF['Coins List'].values.tolist()

        today = datetime.date.today()
        coin_transaction_date = st.date_input('Date: ', today)
        exchange = st.selectbox("Exchange: ", ['Binance'])
        coinName = st.selectbox("Coin Name: ", coinListDF)

        st.info("__Buy__")
        buyPrice = st.number_input("Price: ", 0.0, value=0.0, key=0)
        boughtUnits = st.number_input("Units: ", 0.0, value=0.0, key=0)
        totalCost = buyPrice * boughtUnits
        
        sellPrice, soldUnits, totalSales, profit = 0,0,0,0

        if st.button('Add'):
            add_data(coin_transaction_date, exchange, coinName, buyPrice, boughtUnits, totalCost, sellPrice, soldUnits, totalSales, profit)
            st.success("Added {}".format(coinName))          

        result = view_all_data()
        df = pd.DataFrame(result, columns=['Date', 'Exchange', 'Coin Name', 'Buy Price', 'Bought Units', 'Total Cost', 'Sell Price', 'Sold Units', 'Total Sales', 'Profit'])
        st.dataframe(df)

def sell_coin():
    coinListDF = pd.read_excel('data/Coin List.xlsx', engine='openpyxl')  
    coinListDF = coinListDF['Coins List'].values.tolist()

    with st.beta_expander("Sell Coins"):
        list_of_coins = [i[2] for i in view_all_data()]
        selected_coin = st.selectbox("Choose a coin to update: ", list_of_coins)
        coin_result = get_coin_by_name(selected_coin)
        if coin_result:
            totalCost = coin_result[0][5]

            sellPrice = st.number_input("Update Sell Units:", 0.0, value=0.0)
            soldUnits = st.number_input("Update Sold Units:", 0.0, value=0.0)
            totalSales = sellPrice * soldUnits
            profit = totalSales - float(totalCost)
        
        if st.button('Sell'):
            edit_coin_data(sellPrice, soldUnits, totalSales, profit, selected_coin)
            st.success("Updated {}".format(selected_coin))

def delete_coin():
    with st.beta_expander("Delete Coin"):
        result = view_all_data()
        df = pd.DataFrame(result)
        st.dataframe(df)
        coinList = [i[2] for i in view_all_data()]
        coinName = st.selectbox("Coin to Delete", coinList)
        
        if st.button("Delete"):
            delete_data(coinName)
            st.warning("Deleted {}".format(coinName))
            
        finalResult = view_all_data()
        new_df = pd.DataFrame(finalResult)
        st.dataframe(new_df)