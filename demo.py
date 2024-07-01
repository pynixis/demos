# pip install finance
import yfinance as yf
import sys
import streamlit as st
import pandas as pd
import requests
import yahoo_fin.stock_info as si

# Pilot ApP
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="PPPMF")
from geopy.distance import geodesic

st.set_page_config(layout="wide")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Weather", "TN State Parks", "TN Airports", "Crypto Dashboard", "Currency Dashboard", "Commodities Dashboard", "FDX Stock Data", "Pilot Pay App"])


with tab1:
    st.title("Regional Weather")
    region_weather = pd.read_html(f'https://www.weather.gov/meg/currentweather')

    st.table(region_weather[4])

with tab2:
    st.title("TN State Parks")
    df= pd.read_html(f'https://en.wikipedia.org/wiki/List_of_Tennessee_state_parks')
#print(df['Park Name'])
# To Convert HTML to local CSV file
#df[0].to_csv('tn_state_parks.csv', index=False)
#df= pd.read_csv('tn_state_parks.csv')
#dfs= (df[['ParkName', 'Acres']])

    st.write("State Parks")
    st.table(df[0])
    st.write("State Natural Areas")
    st.table(df[1])

with tab3:
    st.title("TN Airports")

    map_data = pd.read_json("sample_airport_dater.json")

    st.map(map_data, color='#FFA500', zoom=7)

with tab4:
    st.title("Currency/Crypto Live Data")


    url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'

#get html first with get function from requests lib 
    html = requests.get(url).content

#pass html into read_html() function
    crypto_list = pd.read_html(html)

# index 0 will get you the first table available on the page
# index -1 will get you the last table available on the page
    crypto = crypto_list[0]

    st.table(crypto)

with tab5:
    st.title("USD to MXN")

# getting the currency rate for turkish lira
    currency = pd.read_html(f'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MXN')

# prints all the tables
    st.table(currency[0])

with tab6:
    st.title("Commodities Dashboard")
#st.sidebar.header("Memphis Built")
    fdx = yf.Ticker('FDX')
    oil = yf.Ticker('CL=F')
    gold = yf.Ticker('GC=F')
    plat = yf.Ticker('PL=F')
    silver = yf.Ticker('SI=F')
    copper = yf.Ticker('HG=F')


# use "period" instead of start/end
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# (optional, default is '1mo')
    period = '1y'
    hist_fdx = fdx.history(period)
    hist_gold = gold.history(period)
    hist_plat = plat.history(period)
    hist_silver = silver.history(period)
    hist_copper = copper.history(period)
    hist_oil = oil.history(period)

    col1, col2 = st.columns(2)

# plots the graph
    col1.subheader("FDX")
    col1.line_chart(hist_fdx, x=None,y=['Close'])

    col2.subheader("Oil")
#plot the graph
    col2.line_chart(hist_oil, x=None,y=['Close'])

    col1, col2 = st.columns(2)

# plots the graph
    col1.subheader("Gold")
    col1.line_chart(hist_gold, x=None,y=['Close'])

    col2.subheader("Platinum")
#plot the graph
    col2.line_chart(hist_plat, x=None,y=['Close'])

    col1, col2 = st.columns(2)

# plots the graph
    col1.subheader("Silver")
    col1.line_chart(hist_silver, x=None,y=['Close'])

    col2.subheader("Copper")
#plot the graph
    col2.line_chart(hist_copper, x=None,y=['Close'])

with tab7:
    st.title("FDX Stock Data")

# institutionial_holders
    st.table(fdx.institutional_holders)

    company = ['FDX']
    insider = pd.read_html(f'http://openinsider.com/search?q={company}')

    executives = insider[11]
    st.table(executives)
#executives.to_csv('insider.csv')

# get all general stock info
#outputting json
#st.write(fdx.info)

# get stats 
#    fdx_stats = si.get_stats_valuation("FDX")
#    st.table(fdx_stats)

with tab8:
    st.title("Pilot Pay Per Mile Flown")

    st.write("Average flight is 500 miles/hr.")
    st.write("Average Pilot pay is $250/hr.")
    price_mile = float(0.5)

#departure = st.text_input("Departure(Enter city, state)")
#arrival = st.text_input("Arrival(Enter city, state)")

    departure = st.selectbox("Departure", ["Nashville, TN", "Memphis, TN", "New York, NY", "Denver, CO", "Tokyo, JP", "Dubai, UAE", "London, UK"])
    arrival = st.selectbox("Arrival", ["Nashville, TN", "Memphis, TN", "New York, NY", "Denver, CO", "Tokyo, JP", "Dubai, UAE", "London, UK"])



#arrival = input('Enter city, state(start point):')
#dest = input('Enter city, state(end point):')

    start = geolocator.geocode(f'{departure}')
    finish = geolocator.geocode(f'{arrival}')

# Used this to beta test that I was getting the proper output
# print(start)
    begin = (start.latitude, start.longitude)
    end = (finish.latitude, finish.longitude)


    miles = round(geodesic(begin, end).miles,2)

# total_cost = (miles * float(weight) * price_weight * price_mile)

    total_cost = (miles * price_mile)

    st.write(f'Pilot will be paid: $' + str(total_cost), 'for this flight')



