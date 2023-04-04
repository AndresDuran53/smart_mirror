import requests
import json

class OpenWeatherMap():
    weather_url = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self,latitude,longitude,weather_unit,weather_api_token):
        self.latitude = latitude
        self.longitude = longitude
        self.weather_unit = weather_unit
        self.weather_api_token = weather_api_token        

    def get_weather(self):
        weather_req_url = f"{self.weather_url}?units={self.weather_unit}&lat={self.latitude}&lon={self.longitude}&APPID={self.weather_api_token}"
        r = requests.get(weather_req_url)
        weather_obj = json.loads(r.text)
        return weather_obj
    
    def get_temperatur_from_obj(self,weather_obj=None):
        if(weather_obj==None):
            weather_obj = self.get_weather()

        tempAux = weather_obj["main"]["temp"]
        degree_sign= u'\N{DEGREE SIGN}'
        temperature = "%s%s" % (str(tempAux), degree_sign)
        return temperature
    
    def get_icon_id_from_obj(self,weather_obj=None):
        if(weather_obj==None):
            weather_obj = self.get_weather()
        icon_id = weather_obj["weather"][0]["icon"]
        return icon_id
    
    def get_forecast_from_obj(self,weather_obj=None):
        if(weather_obj==None):
            weather_obj = self.get_weather()
        actual_forecast = weather_obj["weather"][0]["main"]
        return self.forecast_to_spanish(actual_forecast)
    
    def forecast_to_spanish(self,forecast):
        forecast_dict = {
            "thunderstorm": "Tormenta",
            "drizzle": "Llovizna",
            "rain": "Lluvia",
            "snow": "Nieve",
            "clear": "Despejado",
            "clouds": "Nublado",
            "fog": "Nublado",
            "haze": "Nublado",
            "mist": "Nublado",
            "dust": "Nublado",
            "squall": "Nublado",
            "ash": "Nublado"
        }
        new_forecast_name = forecast_dict.get(forecast.lower(), forecast)    
        return new_forecast_name
    
    @staticmethod
    def from_json(json_data):
        return OpenWeatherMap(
            json_data['openWeather']['latitude'],
            json_data['openWeather']['longitude'],
            json_data['openWeather']['weather_unit'],
            json_data['openWeather']['weather_api_token']
        )

