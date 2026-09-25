from DataClasses import DA_PowerPrices
import pandas as pd
import requests
import datetime

#TODO: Transform in function to be called from main

#Source for the extraction is Energy-charts. Other sources evaluated but:
# entso-e even after email request there is a bug persisting with authorization. Seems common problem as read in forum
# SMARD -> The request for datetime works and returns time in UNIX but the get for the prices returns error
# ONYX -> even if the web documentation mentions availability of 15-min prices, parameter resolution only accepts hourly/daily
    #no workaround was found on SMARD


#E:extract
#string date of today/tomorrow for parametric url

yesterdaysdate= (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
todaysdate= datetime.datetime.now().strftime("%Y-%m-%d")
tomorrowsdate= (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

base_url = "https://api.energy-charts.info/price"
params= {
    "bzn": "DE-LU",
    "start": todaysdate,
    "end": tomorrowsdate,
}

response_=requests.get( base_url, params=params)
#url = f"https://api.energy-charts.info/price?bzn=DE-LU&start={todaysdate}&end=2026-09-26"
#response = requests.get(url)
response_.raise_for_status()

#T:transform
data = response_.json()

#TODO: convert unix into timeseries
# TODO: create pd.dataframe with timeseries as index and price as column

#df = pd.to_datetime(data["unix_seconds"], unit='s', utc=True)
#df ["price"] = data["price"]

df = pd.DataFrame({
    "timestamp": pd.to_datetime(
        data["unix_seconds"],
        unit="s",
        utc=True
    ).tz_convert("Europe/Berlin"), #converting in Europe Berlin optional, so far I leave it here
    "price": data["price"]
})

target_date = pd.Timestamp(todaysdate, tz="Europe/Berlin")

df = df[
    (df["timestamp"] >= target_date) &
    (df["timestamp"] < target_date + pd.Timedelta(days=1))
]

German_DAprices = DA_PowerPrices(
    data = df,
    MarketArea = params ["bzn"],
    Exchange = "EPEX SPOT"
)



print ("todaysdate: ", todaysdate)
