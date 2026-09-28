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

def get_da_prices (target_date: datetime.date = None, bidzone: str = "DE-LU"):

    yesterdaysdate= (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    #todaysdate= datetime.datetime.now().strftime("%Y-%m-%d")

    if target_date == None:
        target_date = datetime.datetime.now().date() #todays prices

    day_after_target= (target_date + datetime.timedelta(days=1))

    base_url = "https://api.energy-charts.info/price"
    params= {
        "bzn": bidzone,
        "start": target_date.strftime("%Y-%m-%d"),    #transform dates into strings for API call
        "end": day_after_target.strftime("%Y-%m-%d"),
    }

    response_=requests.get( base_url, params=params)
    #url = f"https://api.energy-charts.info/price?bzn=DE-LU&start={target_date}&end=2026-09-26"
    #response = requests.get(url)
    response_.raise_for_status()

    #T:transform
    data = response_.json()

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(
            data["unix_seconds"],
            unit="s",
            utc=True
        ).tz_convert("Europe/Berlin"), #converting in Europe Berlin optional, so far I leave it here
        "price": data["price"]
    })

    target_date_pd = pd.Timestamp(target_date, tz="Europe/Berlin")

    df = df[
        (df["timestamp"] >= target_date_pd) &
        (df["timestamp"] < target_date_pd + pd.Timedelta(days=1))
    ]

    DA_prices = DA_PowerPrices(
        data = df,
        MarketArea = params ["bzn"],
        Exchange = "EPEX SPOT"
    )
    return DA_prices

#test the function
tomorrow_ = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
tomorrow_str=tomorrow_.strftime("%Y-%m-%d")

today_= datetime.datetime.now().date()


DA_prices = get_da_prices(today_, bidzone="DE-LU")

#print ("target_date: ", tomorrow_str)
print ("DA_prices: ", DA_prices)