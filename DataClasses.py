from dataclasses import dataclass
import pandas as pd

@dataclass
class DailyWeather:
    data: pd.DataFrame
    latitude: float
    longitude: float
    elevation: float
    timezone: str

