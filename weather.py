__author__ = 'chernuhaiv'

import pyowm
import datetime

"""
Weather service API.
"""

def get_weather(api_key, location, date):
    """
        :param location : City name || latitude, magnitude values
        :type location: str || map
        :param date : date for predicting weather
        :type date: python.datetime.datetime
        :return
    """

    owm = pyowm.OWM(api_key)

    # parse location
    try:
        if isinstance(location, str) :
            forecast = owm.daily_forecast(location)
            # else coordinates was passed
        else:
            forecast = owm.daily_forecast_at_coords(location['lat'], location['lot'])

    except Exception as e:
        return "Weather couldn't be obtain."

    # get weather
    w = forecast.get_weather_at(location)

    print(w)
    return get_readable_weather(w)


def get_readable_weather(weather):
    """"
        :param weather: Weather object contains weather data
        :type weather : pyowm.webapi25.weather.Weather
        :return: str , can be read by human
    """

