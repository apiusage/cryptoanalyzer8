import streamlit as st
from db import *
import pandas as pd
import requests
import json
import pytz
import tzlocal
import datetime
from datetime import date
from datetime import timedelta

def run_potentialCoin():
    st.header("Potential Coin")
    intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
               "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]

    marketpairsList = []
    dataMarketPairs = GetMarketPairs()
    for i in range(0, len(dataMarketPairs['symbols'])):
        marketpairsList.append(dataMarketPairs['symbols'][i]['symbol'])

    coinOption = st.multiselect("Select a coin", marketpairsList, default="MATICUSDT")
    intervalOption = st.select_slider('Select a interval', options=intervals, value ='1h')
    today = date.today()
    min_date = today
    max_date = today
    startEndDate = st.date_input("Pick a date", (min_date, max_date))
    sDate = startEndDate[0].strftime("%Y/%m/%d, %H:%M:%S")
    eDate = (startEndDate[1] + timedelta(days=1)).strftime("%Y/%m/%d, %H:%M:%S")

    col1, col2 = st.beta_columns(2)

    if coinOption:
        ResultsAll = pd.DataFrame()
        dataJson = GetResultsJson(coinOption, intervalOption)
        for i in range(0, len(dataJson)):
            current_utc_time = pd.to_datetime(dataJson[i][0], unit='ms')

            # UTC time to local time
            local_timezone = tzlocal.get_localzone()
            date_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone('Asia/Singapore')
            dayofweek = dow(date_time)
            date_time = date_time.strftime("%Y/%m/%d, %H:%M:%S")

            close = "{:.4f}".format(float(dataJson[i][4]))
            volume = "{:.2f}".format(float(dataJson[i][5]))

            ResultsData = {'Day': dayofweek, 'Open time': date_time, 'Close': close, 'Volume': volume}
            ResultsAll = ResultsAll.append(ResultsData, ignore_index=True)

        openTime = ResultsAll['Open time'].values.tolist()
        close = ResultsAll['Close'].values.tolist()
        lineChartDF = pd.DataFrame({
            'date': openTime,
            'close': close
        })
        lineChartDF = lineChartDF.set_index('date')
        lineChartDF.sort_values(by="date", inplace=True, ascending=False)
        # st.line_chart(lineChartDF.head(15), use_container_width=True)
        ResultsAll.set_index('Open time', inplace=True)

        dateFilteredDT = ResultsAll[(ResultsAll.index.get_level_values(0) >= sDate) & (ResultsAll.index.get_level_values(0) <= eDate)]
        with col1:
            st.dataframe(ResultsAll)
            st.info("Highest Price")
            column = dateFilteredDT['Close']
            max_value = column.max()
            highest_DF = dateFilteredDT[dateFilteredDT['Close'] == max_value]
            st.dataframe(highest_DF)
        with col2:
            st.dataframe(ResultsAll)
            st.info("Lowest Price")
            column = dateFilteredDT['Close']
            min_value = column.min()
            lowest_DF = dateFilteredDT[dateFilteredDT['Close'] == min_value]
            st.dataframe(lowest_DF)

def GetResultsJson(coinOption, intervalOption):
    # convert requests response to json
    result = requests.get('https://api1.binance.com/api/v3/klines?symbol='+str(coinOption[0])+'&interval='+str(intervalOption))
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

def dow(date):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayNumber = date.weekday()
    return days[dayNumber]


