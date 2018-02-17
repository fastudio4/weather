import requests
import json

class CurentWeather:

    _url = 'http://api.openweathermap.org/data/2.5/weather?'

    def __init__(self, key, units=True):
        '''
            units=True > Temperature in Celsius
            units=False > Temperature in Fahrenheit
        '''
        self.key = '&APPID=' + key
        self.units = self.units(units)


    def units(self, units):
        if isinstance(units, bool):
            return '&units=metric' if units else '&units=imperial'

    def coordinates(self):
        '''
            Auto detect location
        :return: latitude and longitude for API openweathermap
        '''
        raw = requests.get('http://freegeoip.net/json')
        all_data = json.loads(raw.text)
        location = 'lat=%s&lon=%s' % (all_data['latitude'], all_data['longitude'])
        return location

    def request(self):
        response = requests.get(self._url + self.coordinates() + self.units + self.key)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    @property
    def result(self):
        data = self.request()
        if data:
            weather = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind': data['wind']['speed']
                }
            return weather
        else:
            return None
