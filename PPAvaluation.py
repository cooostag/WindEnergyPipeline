#import libraries
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime, time

#import classes and functions from other files
from DataClasses import *
from ImportEPEX import get_da_prices
from ImportWeather import get_target_day_weather
from Wgeneration import calculate_generation
from PPAs import *

#TODO: SUM the P&L

#0. market results are published at 13 CET so I am introducing a if statement to allocate the target date properly
if datetime.now(ZoneInfo("CET")).time() < time(13, 30):  #before 13:30 CET, use today as target date
    target_date = pd.Timestamp.today().normalize()

else: #after 13:30 CET, use tomorrow as target date
    target_date = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)

#1. import weather forecast for either tomorrow or today
target_days_weather = get_target_day_weather(target_date)

#2. calculate wind power generation for tomorrow
Wasset_targetday_generation= calculate_generation(target_days_weather.data)

#3. import day-ahead prices for tomorrow
DA_prices = get_da_prices(target_date.date(), bidzone="DE-LU")

print ("DA_prices index print:",DA_prices.data.index)
print ("Wasset_gen index print:",Wasset_targetday_generation.index)


print ("prices", DA_prices.data)

#4. calculate PPA revenue for tomorrow

Fixed_PPA_Contract1 = FixedPricePPA_asProduced(
    ppa_id="PPA001",
    project_name="Hamburg1",
    project_location="DE-LU",
    project_capacity_numberAssets=1,
    ppa_start_date="2026-09-01",
    ppa_end_date="2026-23-31",
    offtaker_name="Offtaker1",
    offtaker_credit_rating="AAA",
    price_mwh=50.0,
    direction_type="sell",
    direction_multiplier=int(1)
)

#create a dataframe with output : [Time, Generation, Market Price, PPA price, Revenue, P&L]

def PPA_valuation (PPA_contract: PPA, Asset_generation: pd.DataFrame, Market_price: pd.DataFrame
                   ) -> pd.DataFrame:
    #create / copy the generation forecast and make it my base valuation df
    df = Asset_generation.copy()

    # add the column with market prices with join
    #need to correct timezone issue into weather forecast import
    df = df.join (Market_price[["price"]], how="left")
    #rename to DA market price
    df = df.rename(columns={"price": "DA_price"})

    #create a column with PPA price
    df ["PPA_price"] = PPA_contract.price_mwh

    #compute revenue = generation * PPA price
    df ["Revenue"] = 0.25*df["power_output"] * df["PPA_price"] / 1000

    #compute P&L = revenue - (generation * market price)
    df ["P&L"] = 0.25*(df["PPA_price"] - df["DA_price"]) * df["power_output"] /1000

    return df

Valuation_df = PPA_valuation (Fixed_PPA_Contract1, Wasset_targetday_generation, DA_prices.data)

print ("test")