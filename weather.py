__author__ = 'chernuhaiv'

import pyowm

"""
Weather service API.
"""

owm = pyowm.OWM('')

def get_forecast(location):
    # parse location
    try:
        if isinstance(location, str) :
            forecast = owm.daily_forecast(location)
            # else coordinates was passed
        else:
            forecast = owm.daily_forecast_at_coords(location['lat'], location['lot'])
        return forecast
    except Exception as e:
        return None

def get_weather(location, date):
    """
        :param location : City name || latitude, magnitude values
        :type location: str || map
        :param date : date for predicting weather
        :type date: python.datetime.datetime
        :return simple weather info
    """
    forecast = get_forecast(location)
    if  forecast == None :
        return "Weather couldn't be obtain."

    try:
        w = forecast.get_weather_at(date)
        return w.get_status()

    except Exception as e:
        return "Weather couldn't be obtain."

def get_weather_verbose(location, date):
    """
        :param location : City name || latitude, magnitude values
        :type location: str || map
        :param date : date for predicting weather
        :type date: python.datetime.datetime
        :return weather info about temperature
    """

    forecast = get_forecast(location)
    if  forecast == None :
        return "Weather couldn't be obtain."

    # get weather
    try:
        w = forecast.get_weather_at(date)
        return get_readable_weather(w)

    except Exception as e:
        return "Weather couldn't be obtain."

def get_weather_very_verbose(location, date):
    """
        :param location : City name || latitude, magnitude values
        :type location: str || map
        :param date : date for predicting weather
        :type date: python.datetime.datetime
        :return detailed weather info about temperature, humidity, shiness
    """
    forecast = get_forecast(location)
    if  forecast == None :
        return "Weather couldn't be obtain."

    # get weather
    try:
        verb_str = get_weather_verbose(location, date)
        w = forecast.get_weather_at(date)
        return verb_str + get_readable_weather_very_verbose(w)
    except Exception as e:
        return "Weather couldn't be obtain."

def get_readable_weather(weather):
    """"
        :param weather: Weather object contains weather data
        :type weather : pyowm.webapi25.weather.Weather
        :return: str , can be read by human
    """
    temp_ = weather.get_temperature('celsius')['day']
    temp_ = "{0:.0f}".format(round(temp_))
    status_ = weather.get_detailed_status()
    return "{status} weather. The temperature is {temp} in degrees Celsius. "\
        .format(status=status_,temp=temp_)

def get_readable_weather_very_verbose(weather):
    """"
        :param weather: Weather object contains weather data
        :type weather : pyowm.webapi25.weather.Weather
        :return: str , can be read by human
    """
    res = ""
    clouds_ = weather.get_clouds()
    if clouds_ > 0 :
        res += "Clouds coverage is {clouds} percents. ".format(clouds=clouds_)
    rain_ = weather.get_rain()
    if rain_ != {}:
        res += "Precipitations are {rain} rate. ".format(rain=rain_['all'])
    snow_ = weather.get_snow()
    if snow_ != {}:
        snow_ = "{0:.0f}".format(round(snow_['all']))
        res += "Snow rate is {snow}. ".format(snow=snow_)
    wind_ = weather.get_wind()
    if wind_ != {}:
        res += "Wind speed is {wind}. ".format(wind=wind_)
    humidity_ = weather.get_humidity()
    if humidity_ != {}:
        res += "Humidity is {humidity} repcents. ".format(humidity=humidity_)
    pressure_ = weather.get_pressure()['press'] - 70
    pressure_ = "{0:.0f}".format(round(pressure_))

    res += "Pressure value is {pressure}. ".format(pressure=pressure_)
    return res
