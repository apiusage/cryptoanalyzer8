import streamlit as st
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        cryptoDB ( \
            coinName TEXT, \
            price TEXT, \
            units TEXT, \
            TotalCost TEXT \
        )')

def add_data(*data):
    c.execute('INSERT INTO cryptoDB (coinName, price, units, TotalCost) \
        VALUES (?,?,?,?)', data)
    conn.commit()

def view_all_data():
    c.execute('SELECT * FROM cryptoDB')
    data = c.fetchall()
    return data

def get_product_by_name(product):
    c.execute('SELECT * FROM startupIdea WHERE product = "{}"'.format(product))
    data = c.fetchall()
    return data

def edit_product_data(*updatedData):
    c.execute("UPDATE startupIdea SET \
                customerProblem=?,\
                productFeatures=?,\
                business_model=?,\
                product=?,\
                hair_on_fire_factor=?,\
                access_to_market=?,\
                day_1_revenue=?,\
                revenueScalability=?,\
                defensibility=?,\
                lackofCompetitors=?,\
                personal_Passion=?, \
                unfair_Advantage=?, \
                ipCreation=?, \
                acquisition_Potential=? WHERE \
                product=?", updatedData)
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(product):
    c.execute('DELETE FROM startupIdea WHERE product = "{}"'.format(product))
    conn.commit()