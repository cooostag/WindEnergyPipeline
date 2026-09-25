from dataclasses import dataclass
from typing import Optional

import pandas as pd

@dataclass
class DailyWeather:
    data: pd.DataFrame
    latitude: Optional[float]
    longitude: Optional[float]
    elevation: Optional[float]
    timezone: Optional[str]

@dataclass
class DA_PowerPrices:
    data: pd.DataFrame
    MarketArea: Optional [str]
    Exchange: Optional [str]

