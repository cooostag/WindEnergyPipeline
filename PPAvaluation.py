#import libraries
import pandas as pd

#import classes and fuctions from other files
from DataClasses import *
from ImportEPEX import get_da_prices
from ImportWeather import get_target_day_weather
from Wgeneration import calculate_generation
from PPAs import *

#1. import weather forecast for tomorrow
Tomorrow = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
target_days_weather = get_target_day_weather(Tomorrow)

#2. calculate wind power generation for tomorrow
Wasset_targetday_generation= calculate_generation(target_days_weather.data)

#3. import day-ahead prices for tomorrow
DA_prices = get_da_prices(Tomorrow.date(), bidzone="DE-LU")

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

def PPA_valuation ( PPA_contarct: PPA, Asset_generation: pd.DataFrame, Market_price: pd.DataFrame
                    ) -> pd.DataFrame:
    #create / copy the generation forecast and make it my base valuation df
    df = Asset_generation.copy()

    # add the column with market prices with join
    #need to correct timezone issue into weather forecast import
    df = df.join (Market_price[["price"]], how="left")

    #create a column with PPA price
    df ["PPA_price"] = PPA_contarct.price_mwh

    #compute revenue = generation * PPA price
    df ["Revenue"] = df["power_output"] * df["PPA_price"]

    #compute P&L = revenue - (generation * market price)

    return df

Valuation_df = PPA_valuation (Fixed_PPA_Contract1, Wasset_targetday_generation, DA_prices.data)

print ("test")