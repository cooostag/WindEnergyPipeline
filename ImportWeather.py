#import weather data here

from DataClasses import DailyWeather
import pandas as pd
import requests
import datetime

#TODO: Transform in function to be called from main

def get_target_day_weather(target_day: datetime.date = None):
    #E:extract
    url = "https://api.open-meteo.com/v1/forecast?latitude=53.5&longitude=9.9&minutely_15=wind_speed_80m,temperature_2m,precipitation&forecast_minutely_15=192"
    response = requests.get(url)
    response.raise_for_status()

    #T:transform
    data = response.json()

    #separate the observables timeseries into a dataframe and set the time as index
    df=pd.DataFrame(data["minutely_15"])

    df["time"] = pd.to_datetime(df["time"])

    #drop of observables for days that are not tomorrow
    #tomorrow = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
    day_after_target = target_day + pd.Timedelta(days=1)

    df = df[
        (df["time"] >= target_day) &
        (df["time"] < day_after_target)
    ].set_index("time")

    #L:Load into final data object

    target_days_weather = DailyWeather(
        data = df,
        latitude = data["latitude"],
        longitude = data["longitude"],
        elevation = data["elevation"],
        timezone = data["timezone"]
    )
    return target_days_weather

#test the function
tomorrows_weather_ =     tomorrow = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
target_days_weather = get_target_day_weather(tomorrows_weather_)

#print ("success")
print("target_days_weather: ", target_days_weather)