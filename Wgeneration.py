from DataClasses import *
import pandas as pd
import requests
import datetime
from ImportWeather import get_target_day_weather

def calculate_generation(
    df: pd.DataFrame,
    rated_power: float = 3000,
    cut_in: float = 3,
    rated_wind_speed: float = 12,
    cut_out: float = 25,
) -> pd.DataFrame:

    df_generation = df.copy()
    wind_speed = df_generation["wind_speed_80m"]
    df_generation["power_output"] = 0.0 #initialize the power output column = 0.0 (float) and then changing values where there is output expected

    #wind speed < than cut in speed
    mask = (wind_speed >= cut_in) & (wind_speed < rated_wind_speed)

    df_generation.loc[mask, "power_output"] = (
        rated_power
        * (wind_speed[mask] - cut_in)
        / (rated_wind_speed - cut_in)
    )

    # Between rated wind speed and cut-out
    mask = (wind_speed >= rated_wind_speed) & (wind_speed <= cut_out)

    df_generation.loc[mask, "power_output"] = rated_power

    return df_generation


#test the file
tomorrows_weather_ =     tomorrow = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
target_days_weather = get_target_day_weather(tomorrows_weather_)

Wasset_targetday_generation= calculate_generation(target_days_weather.data)

print ("Wasset_targetday_generation: ", Wasset_targetday_generation)
print (Wasset_targetday_generation.head())
print (Wasset_targetday_generation.shape)