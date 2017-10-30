import requests
import json

def get_weather():
    #get config from heroku config vars
    config = json.loads(environ[name])

    api_key = config["weather-map-api-key"]
    url = 'https://api.openweathermap.org/data/2.5/weather?id=2894003&lang=de&units=metric&APPID=' + api_key #weather for Kaiserslautern
    response = requests.request("GET", url).json()
    return "In Kaiserslautern ist es " + func(response['weather'][0]['description']) + " bei " + "{:.1f}".format(response['main']['temp']).replace('.', ',') + " Grad Celcius."

func = lambda s: s[:1].lower() + s[1:] if s else ''