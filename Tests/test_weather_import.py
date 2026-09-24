import pandas as pd

from ImportWeather import tomorrows_weather as weather


def test_import_weather():
    assert len(weather.data) == 96
    assert weather.data.index.is_unique
    assert weather.data.index.to_series().diff().dropna().eq(
        pd.Timedelta(minutes=15)
    ).all()