from datetime import datetime
import requests

def kelvin_to_celsius(K):
    return int(K-273.15)

def kelvin_to_fahrenheit(K):
    return int(K*(9/5)-459.67)

def timestamp_to_datetime(ts,timezone_offset=0):
    ts=ts+timezone_offset
    return datetime.fromtimestamp(ts).strftime("%m/%d %H:%M")

def get_daily_forecast(daily_list):
    forecast_list = []
    for item in daily_list[:-3]:
        D = dict()
        D['datetime'] = timestamp_to_datetime(item['dt'])[:5]
        D['celsius'] = kelvin_to_celsius(item['feels_like']['day'])
        D['fahrenheit'] = kelvin_to_fahrenheit(item['feels_like']['day'])
        D['uvi'] = item['uvi']
        forecast_list.append(D)
    return forecast_list

def forecast_api_request(response, API_KEY):
    weather_dict = dict()
    lon = response['coord']['lon']
    lat = response['coord']['lat']
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly&appid={}'\
        .format(lat, lon, API_KEY)
    forecast_response = requests.get(url).json()
    weather_dict = {
            'current': [{
                        'city' : response['name'].title(),
                        'country': response['sys']['country'].upper(),
                        'celsius': kelvin_to_celsius(response['main']['feels_like']),
                        'fahrenheit': kelvin_to_fahrenheit(response['main']['feels_like']),
                        'uvi': forecast_response['current']['uvi'],
                        'description': response['weather'][0]['description'],
                        'iconcode': response['weather'][0]['id'],
                        'datetime': timestamp_to_datetime(forecast_response['current']['dt'],
                                                          forecast_response['timezone_offset']
                                                          )
                        }],
            'forecast': get_daily_forecast(forecast_response['daily'])
        }
    return weather_dict