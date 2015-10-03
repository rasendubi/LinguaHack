__author__ = 'chernuhaiv, tsutsarin'

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
        :param location : City name || 'lat', 'lot' values
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
        :param location : City name || 'lat', 'lot' values
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
        :param location : City name || 'lat', 'lot' values
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
    
def will_be_weather(location, date, weather_type):
    """
        :param location : City name || 'lat', 'lot' values
        :type location: str || map
        :param date : date for predicting weather
        :type date: python.datetime.datetime
        :param weather_type: weather condition
        :type weather_type: str
        :return boolean about specific weather condition at given location and date
    """
    fc = owm.daily_forecast(location)
    return {
        'cloudy': fc.will_be_cloudy_at(date),
        'foggy': fc.will_be_foggy_at(date),
        'hurricane': fc.will_be_hurricane_at(date),
        'rainy': fc.will_be_rainy_at(date),
        'snowy': fc.will_be_snowy_at(date),
        'stormy': fc.will_be_stormy_at(date),
        'sunny': fc.will_be_sunny_at(date),
        'tornado': fc.will_be_tornado_at(date),
    }[weather_type]


def will_have_weather(location, weather_type):
    """
        :param location : City name || 'lat', 'lot' values
        :type location: str || map
        :param weather_type: weather condition
        :type weather_type: str
        :return boolean about specific weather condition at given location and forecast period
    """
    fc = owm.daily_forecast(location)
    return {
        'cloudy': fc.will_have_clouds(),
        'foggy': fc.will_have_fog(),
        'hurricane': fc.will_have_hurricane(),
        'rainy': fc.will_have_rain(),
        'snowy': fc.will_have_snow(),
        'stormy': fc.will_have_storm(),
        'sunny': fc.will_have_sun(),
        'tornado': fc.will_have_tornado(),
    }[weather_type]


def when_weather(location, weather_type):
    """
        :param location : City name || 'lat', 'lot' values
        :type location: str || map
        :param weather_type: weather condition
        :type weather_type: str
        :return datetime.datetime object list when weather condition occurs 
    """
    fc = owm.daily_forecast(location)
    weathers = {
        'cloudy': fc.when_clouds(),
        'foggy': fc.when_fog(),
        'hurricane': fc.when_hurricane(),
        'rainy': fc.when_rain(),
        'snowy': fc.when_snow(),
        'stormy': fc.when_storm(),
        'sunny': fc.when_sun(),
        'tornado': fc.when_tornado(),
    }[weather_type]

    # UNIX datestamps of weather measurement
    unix_dates = map(lambda x: x.get_reference_time(), weathers)

    # datetime.datetime objects
    date_dates = map(lambda x: pyowm.utils.timeformatutils.to_date(x), unix_dates)

    return date_dates

# Some functions are not implemented right in the pyowm library
def most_weather(location, weather_type):
    """
        :param location : City name || 'lat', 'lot' values
        :type location: str || map
        :param weather_type: weather condition
        :type weather_type: str
        :return datetime.datetime object when weather condition is most
    """
    fc = owm.daily_forecast(location)
    weather = {
        # Not working in library
        # 'cold': fc.most_cold(),

        # Not working in library
        # 'hot': fc.most_hot(),

        'humid': fc.most_humid(),
        'rainy': fc.most_rainy(),
        'snowy': fc.most_snowy(),

        # Not working in library
        # 'windy': fc.most_windy(),
    }[weather_type]

    if weather:
        unix_weather = weather.get_reference_time()
        date_weather = pyowm.utils.timeformatutils.to_date(unix_weather)
        return date_weather

    return None

