from openweathermap import OpenWeatherMap

from dotenv import load_dotenv
import os
load_dotenv()  

api_key = os.getenv("OPENWEATHER_API_KEY")

def test_get_forecast_200():
    weather_service = OpenWeatherMap(api_key)
    result = weather_service.get_coord_forecast({
        "lat": 51.5074,
        "lon": -0.1278
    }, hours_to_forecast=1)

    # Check if the response contains the expected 'cod' field and that it indicates success
    assert 'cod' in result
    assert result['cod'] == '200'

def test_get_forecast_city_london():
    weather_service = OpenWeatherMap(api_key)
    result = weather_service.get_coord_forecast({
        "lat": 51.5074,
        "lon": -0.1278
    }, hours_to_forecast=1)

    # Check if the response contains the expected 'cod' field and that it indicates success
    assert 'cod' in result
    assert result['cod'] == '200'
    assert 'city' in result
    assert result['city']['name'] == 'London'
    
def test_get_forecast_invalid_coordinates():
    weather_service = OpenWeatherMap(api_key)
    result = weather_service.get_coord_forecast({
        "lat": 999,
        "lon": 999
    }, hours_to_forecast=1)
    
    # Check if the response contains the expected 'cod' field and that it indicates an error
    assert 'cod' in result
    assert result['cod'] != '200'
    assert 'message' in result

if __name__ == "__main__":
    test_get_forecast_200()
    test_get_forecast_city_london()
    test_get_forecast_invalid_coordinates()
    print("All tests passed!")