from db import *
import pandas as pd
import requests
import json
import pytz
from datetime import date, timedelta
import plotly.express as px
from pandas import read_excel

def run_potentialCoin():
    st.header("__Potential Coin__")
    intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    marketpairsList = []
    dataMarketPairs = GetMarketPairs()
    for i in range(0, len(dataMarketPairs['symbols'])):
        marketpairsList.append(dataMarketPairs['symbols'][i]['symbol'])
    coinOption = st.multiselect("Select a coin", marketpairsList)
    intervalOption = st.select_slider('Select a interval', options=intervals, value='1h')

    today = date.today()
    min_date = today
    max_date = today
    startEndDate = st.date_input("Pick a date", (min_date, max_date))
    sDate = startEndDate[0].strftime("%Y/%m/%d, %H:%M:%S")
    eDate = (startEndDate[1] + timedelta(days=1)).strftime("%Y/%m/%d, %H:%M:%S")

    col1, col2 = st.beta_columns(2)
    if coinOption:
        closeDF = pd.DataFrame()
        dataJson = GetResultsJson(coinOption, intervalOption)
        for i in range(0, len(dataJson)):
            # UTC time to local time
            current_utc_time = pd.to_datetime(dataJson[i][0], unit='ms')
            date_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone('Asia/Singapore')
            date_time = date_time.strftime("%Y/%m/%d, %H:%M:%S")

            close = "{:.4f}".format(float(dataJson[i][4]))
            closeData = {'Open time': date_time, 'Close': close}
            closeDF = closeDF.append(closeData, ignore_index=True)

        closeDF = closeDF[(closeDF['Open time'] >= sDate) & (closeDF['Open time'] <= eDate)]
        displayLineChart(closeDF)
        closeDF['Day'] = pd.to_datetime(closeDF['Open time']).dt.strftime("%a")
        closeDF.set_index('Open time', inplace=True)

        weekNumber = date.today().isocalendar()[1]
        closeDF['Week'] = pd.DatetimeIndex(closeDF.index).isocalendar().week
        closeDF['Year'] = pd.DatetimeIndex(closeDF.index).isocalendar().year
        with col1:
            st.dataframe(closeDF)
            st.info("__Highest price of each week__" + " (Current week #: " + str(weekNumber) + ")")
            maxCloseDF = closeDF.groupby(['Year', 'Week']).agg({'Close': 'max'})
            highest_value_list = maxCloseDF['Close'].values.tolist()
            out1 = closeDF[closeDF['Close'].isin(highest_value_list)]
            df = out1.sort_values(by=['Close'], ascending=False)
            df = df.drop_duplicates(subset=['Week'], keep='first')
            st.dataframe(df.sort_index(ascending=False))

        with col2:
            st.dataframe(closeDF)
            st.info("__Lowest price of each week__")
            minCloseDF = closeDF.groupby(['Year', 'Week']).agg({'Close': 'min'})
            lowest_value_list = minCloseDF['Close'].values.tolist()
            out2 = closeDF[closeDF['Close'].isin(lowest_value_list)]
            df = out2.sort_values(by=['Close'], ascending=True)
            df = df.drop_duplicates(subset=['Week'], keep='first')
            st.dataframe(df.sort_index(ascending=False))

        my_expander = st.beta_expander(label='Research Sites')
        with my_expander:
            displayDYORSites()

def GetResultsJson(coinOption, intervalOption):
    result = requests.get(
        'https://api1.binance.com/api/v3/klines?symbol=' + str(coinOption[0]) + '&interval=' + str(
            intervalOption) + '&limit=2000')
    if result.ok:
        json_data = json.loads(result.text)
        return json_data
    else:
        GetResultsJson(coinOption)

def GetMarketPairs():
    result = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    if result.ok:
        json_data = json.loads(result.text)
        return json_data

def displayLineChart(closeDF):
    fig = px.line(closeDF, x="Open time", y="Close")
    fig.update_yaxes(autorange="reversed")
    fig.update_yaxes(categoryorder="category descending")
    fig.update_layout(xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

def displayDYORSites():
    my_sheet = 'Sheet1'
    file_name = 'DYOR Sites.xlsx'
    df = read_excel(file_name, sheet_name=my_sheet, engine='openpyxl')
    df.columns = df.columns.str.strip()
    for index, row in df.iterrows():
        link = row['URL']
        name = row['Name']
        url = name + ': {}'.format(link)
        st.write(url)





