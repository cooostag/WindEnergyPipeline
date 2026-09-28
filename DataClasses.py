from dataclasses import dataclass
from typing import Optional

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
    MarketArea: Optional [str]
    Exchange: Optional [str]
