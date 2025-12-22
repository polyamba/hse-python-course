import os
import json
import requests
import tempfile
from time import time

def get_cached_weather_data(city, cache_minutes=10):

    temp_dir = tempfile.gettempdir()
    cache_path = os.path.join(temp_dir, f"weather_{city}.json")
    
    if os.path.exists(cache_path):
        cache_age = time() - os.path.getmtime(cache_path)
        if cache_age < cache_minutes * 60:
            print(f"Используем кэш для {city} (возраст: {cache_age:.0f} сек)")
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Кэш устарел для {city} (возраст: {cache_age:.0f} сек)")
    
    print(f"Запрашиваем данные из API для {city}")

    api_key = 'e347a6927b754af1af5222859252112'
    city_url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes'
    
    try:
        response = requests.get(city_url, timeout=10)
        response.raise_for_status()  
        
        data = response.json()
        
        if 'error' in data:
            print(f"Ошибка API: {data['error']['message']}")
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Данные сохранены в кэш: {cache_path}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")


def cleanup_weather_cache():
    """Очищает все кэш-файлы погоды"""
    
    """Очищает все кэш-файлы погоды"""
    
    temp_dir = tempfile.gettempdir()
    
    for f in os.listdir(temp_dir):
        if f.startswith('weather_') and f.endswith('.json'):
            os.unlink(os.path.join(temp_dir, f))
    
    print("Кэш очищен")

# Использование:
print(get_cached_weather_data("London"))
print(get_cached_weather_data("Moscow"))

cleanup_weather_cache()
