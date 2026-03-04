from datetime import datetime
import requests

class OpenWeatherMap:
    def __init__(self, api_key):
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.api_key = api_key
        

    def get_coord_forecast(self, coord: dict, hours_to_forecast: int = 1) -> dict:

        querystring = {
            "lat": coord.get('lat'),
            "lon": coord.get('lon'),
            "appid": self.api_key,
            "cnt": hours_to_forecast,
            "units": "metric"
        }

        response = requests.get(self.base_url, params=querystring)
        data = response.json()
        
        if response.status_code != 200:
            
            return data
        
        if response.status_code == 200:
            city = data.get('city', None)
            if city:
                city['sun_visible'] = False
                sunrise = city.get('sunrise', None)
                sunset = city.get('sunset', None)
                
                if sunrise:
                    city['sunrise_readable'] = datetime.fromtimestamp(sunrise)
                if sunset:
                    city['sunset_readable'] = datetime.fromtimestamp(sunset)
                    
                if 'sunrise_readable' in city and 'sunset_readable' in city:
                    if city['sunrise_readable'] < datetime.now() < city['sunset_readable']:
                        city['sun_visible'] = True
                    
                data['city'] = city

            return data

        return None