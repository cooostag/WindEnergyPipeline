from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date

import pandas as pd

@dataclass
class Weather:
    data: pd.DataFrame
    latitude: Optional[float]
    longitude: Optional[float]
    elevation: Optional[float]
    timezone: Optional[str]

@dataclass
class ForecastWeather(Weather):
    forecast_horizon: Optional[int] = None

@dataclass
class DA_PowerPrices:
    data: pd.DataFrame
    marketarea: Optional [str]
    exchange: Optional [str]


#create a general future prices object, will be initialized manually with a date´s price from the EEX website
    #in order to construct a forward price curve

@dataclass
class FuturePrices:
    maturity_type : str
    maturity: str
    price : float
    price_date: date
    currency : str
    unit : str
    market_area : str
    start_date: date
    end_date: date


@dataclass
class ForwardPriceCurve:
    market_area: str
    price_date: date
    data: pd.DataFrame
    unit: str
    currency: str
    start_date: date
    end_date: date

#define a function that takes a list of FuturesPrices objects and returns a ForwardPriceCurve object