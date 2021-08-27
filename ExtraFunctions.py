from millify import millify
from streamlit_metrics import metric, metric_row

columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
           "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]

# Volume
volumeDF = pd.DataFrame()
volumeData = {'Open time': date_time, 'Volume': volume}
volumeDF = volumeDF.append(volumeData, ignore_index=True)

# import altair as alt
volumeDF = volumeDF[(volumeDF['Open time'] >= sDate) & (volumeDF['Open time'] <= eDate)]
volumeDF['Open time'] = "(" + pd.to_datetime(volumeDF['Open time']).dt.strftime("%a") + ") " + volumeDF['Open time']
chart = alt.Chart(volumeDF).mark_line().encode(
    x=alt.X('Open time:N', axis=alt.Axis(title='')),
    y=alt.Y('Volume:Q'),
    tooltip='Volume:N'
).properties()
st.altair_chart(chart, use_container_width=True)

def dayTradingCoins():
    dataMarketPairs = GetMarketPairs()
    df = pd.DataFrame()
    for i in range(0, len(dataMarketPairs['symbols'])):
        coinName = dataMarketPairs['symbols'][i]['symbol']
        result = requests.get('https://api1.binance.com/api/v3/klines?symbol='+str(coinName)+'&interval=1m')
        json_data = json.loads(result.text)
        high = float(json_data[0][2])
        low = float(json_data[0][3])
        getPercentage = percentage(low, high)
        coinDetails = {'Coin': coinName, 'Low': "{:.4f}".format(low), 'High': "{:.4f}".format(high), 'Earning %': getPercentage}
        df = df.append(coinDetails, ignore_index=True)

    st.dataframe(df)

def getCoinMarketCap(marketpairsList):
    st.markdown("""---""")
    coin = st.multiselect("Select a coin", marketpairsList, key=1)
    coinString = ''.join(coin)

    df = pd.DataFrame()
    result = requests.get('https://www.binance.com/exchange-api/v2/public/asset-service/product/get-products')
    json_data = json.loads(result.text)
    for i in range(0, len(json_data['data'])):
        coinName = json_data['data'][i]['s']
        circulatingSupply = json_data['data'][i]['cs']
        currentAssetPrice = json_data['data'][i]['c']
        volume = json_data['data'][i]['v']

        coinInfo = {'Coin': coinName, 'Volume': volume, 'Circulating Supply': circulatingSupply, 'Current Price': currentAssetPrice}
        df = df.append(coinInfo, ignore_index=True)

    df['Market Cap'] = df['Circulating Supply'].astype(float).multiply(df['Current Price'].astype(float))
    df['Percentage'] = (df['Volume'].astype(float) / df['Market Cap'].astype(float)) * 100
    df.sort_values(by=['Percentage'], ascending=False, inplace=True)
    df = df.reset_index(drop=True)
    st.dataframe(df[['Coin', 'Percentage']])

    filteredDF = df[(df['Coin'].str.contains(coinString))]
    st.dataframe(filteredDF)

# Order book
getOrderBookInfo(coinOption[0])
def getOrderBookInfo(coinName):
    bidOrderBookDF = pd.DataFrame()
    askOrderBookDF = pd.DataFrame()
    result = requests.get('https://api1.binance.com/api/v3/depth?symbol=' + str(coinName) + '&limit=5000')
    json_data = json.loads(result.text)
    for i in range(0, len(json_data['bids'])):
        bidPrice = float(json_data['bids'][i][0])
        Qty = float(json_data['bids'][i][1])

        bidData = {'Bid': bidPrice, 'Qty': Qty}
        bidOrderBookDF = bidOrderBookDF.append(bidData, ignore_index=True)

    bidOrderBookDF['Total price'] = bidOrderBookDF['Bid'] * bidOrderBookDF['Qty']
    bidOrderBookDF = bidOrderBookDF[(bidOrderBookDF['Total price'] >= 10000)]
    bidOrderBookDF['Qty'] = bidOrderBookDF['Qty'].round()
    bidOrderBookDF['Total price'] = bidOrderBookDF['Total price'].round()

    for i in range(0, len(json_data['asks'])):
        askPrice = float(json_data['asks'][i][0])
        Qty = float(json_data['asks'][i][1])

        askData = {'Ask': askPrice, 'Qty': Qty}
        askOrderBookDF = askOrderBookDF.append(askData, ignore_index=True)

    askOrderBookDF['Total price'] = askOrderBookDF['Ask'] * askOrderBookDF['Qty']
    askOrderBookDF = askOrderBookDF[(askOrderBookDF['Total price'] >= 10000)]
    askOrderBookDF['Qty'] = askOrderBookDF['Qty'].round()
    askOrderBookDF['Total price'] = askOrderBookDF['Total price'].round()

    col1, col2 = st.beta_columns(2)
    with col1:
        st.info("__Support__ - " + getBestBidPriceQty(coinName))
        bidOrderBookDF = bidOrderBookDF.reset_index(drop=True)
        st.dataframe(bidOrderBookDF.sort_values(by=['Bid'], ascending=False))
        totalBids = bidOrderBookDF['Total price'].sum()
    with col2:
        st.info("__Resistance__ - " + getBestAskPriceQty(coinName))
        askOrderBookDF = askOrderBookDF.reset_index(drop=True)
        st.dataframe(askOrderBookDF.sort_values(by=['Ask']))
        totalAsks = askOrderBookDF['Total price'].sum()

    metric_row(
        {
            "Total Bids": millify(totalBids, precision=2),
            "Total Asks": millify(totalAsks, precision=2)
        }
    )

def getBestBidPriceQty(coinName):
    result = requests.get('https://api1.binance.com/api/v3/ticker/bookTicker?symbol=' + str(coinName))
    json_data = json.loads(result.text)
    bidPrice = float(json_data['bidPrice'])
    bidQty = float(json_data['bidQty'])

    bidString = "Best Bid Price: " + str(bidPrice) + " / Qty: " + str(bidQty)
    return bidString

def getBestAskPriceQty(coinName):
    result = requests.get('https://api1.binance.com/api/v3/ticker/bookTicker?symbol=' + str(coinName))
    json_data = json.loads(result.text)
    askPrice = float(json_data['askPrice'])
    askQty = float(json_data['askQty'])

    askString = "Best Ask Price: " + str(askPrice) + " / Qty: " + str(askQty)
    return askString

# Date time
dayofweek = dow(date_time)
def dow(date):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dayNumber = date.weekday()
    return days[dayNumber]


def filterDFDate(DF, sDate, eDate):
    copiedDF = DF.copy()
    copiedDF['Week'] = pd.DatetimeIndex(copiedDF.index).isocalendar().week
    copiedDF['Year'] = pd.DatetimeIndex(copiedDF.index).isocalendar().year
    copiedDF = copiedDF[(copiedDF.index.get_level_values(0) >= sDate) & (copiedDF.index.get_level_values(0) <= eDate)]
    return copiedDF

def getHLAPrice(HighDF, LowDF, coinAvgCost):
    column = HighDF["High"]
    max_value = column.max()
    column = LowDF["Low"]
    min_value = column.min()
    st.info("__Current Avg Price (5 mins):__" + " {:.3f}".format(float(coinAvgCost))+\
             " / __Lowest Price:__" + " {:.3f}".format(float(min_value))+\
             " / __Highest Price:__" + " {:.3f}".format(float(max_value))+\
             " / __Max Earning Percentage:__ " + percentage(min_value, max_value))

coinAvgCost = coinAvgPrice(coinOption[0])
def coinAvgPrice(coinName):
    result = requests.get('https://api1.binance.com/api/v3/avgPrice?symbol='+str(coinName))
    json_data = json.loads(result.text)
    return json_data["price"]

def percentage(part, whole):
    try:
        percentage = 100 * (1-(float(part)/float(whole)))
    except ZeroDivisionError:
        percentage = 0

    return str("{:.2f}".format(percentage)) + "%"

changes24Hours(coinOption[0])
def changes24Hours(coinName):
    result = requests.get('https://api1.binance.com/api/v3/ticker/24hr?symbol=' + str(coinName))
    json_data = json.loads(result.text)
    priceChange = json_data["priceChange"]
    percentChange = json_data["priceChangePercent"]
    lowPrice = json_data["lowPrice"]
    highPrice = json_data["highPrice"]
    weightedAvgPrice = json_data["weightedAvgPrice"]
    volume = int((float(json_data["volume"])))

    st.info("__24 hours change statistics__")
    metric_row(
        {
            "Price Change": millify(priceChange, precision=2),
            "Percent Change": millify(percentChange, precision=2) + "%",
            "Low Price": millify(lowPrice, precision=2),
            "High Price": millify(highPrice, precision=2),
            "Average Price (24 hrs)": millify(weightedAvgPrice, precision=2),
            "Volume (24 hrs)": millify(volume, precision=0)
        }
    )
