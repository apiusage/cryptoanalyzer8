import streamlit as st
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        cryptoDB ( \
            coin_transaction_date DATE, \
            exchange TEXT, \
            coinName TEXT, \
            buyPrice TEXT, \
            boughtUnits TEXT, \
            totalCost TEXT, \
            sellPrice TEXT, \
            soldUnits TEXT, \
            totalSales TEXT, \
            profit TEXT \
        )')

def add_data(*data):
    c.execute('INSERT INTO cryptoDB (coin_transaction_date, exchange, coinName, buyPrice, boughtUnits, totalCost, sellPrice, soldUnits, totalSales, profit) \
        VALUES (?,?,?,?,?,?,?,?,?,?)', data)
    conn.commit()

def view_all_data():
    c.execute('SELECT * FROM cryptoDB')
    data = c.fetchall()
    return data

def get_coin_by_name(coin):
    c.execute('SELECT * FROM cryptoDB WHERE coinName = "{}"'.format(coin))
    data = c.fetchall()
    return data

def edit_coin_data(*updatedData):
    c.execute("UPDATE cryptoDB SET \
                sellPrice=?,\
                soldUnits=?,\
                totalSales=?,\
                profit=? WHERE \
                coinName=?", updatedData)
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(coin):
    c.execute('DELETE FROM cryptoDB WHERE coinName = "{}"'.format(coin))
    conn.commit()