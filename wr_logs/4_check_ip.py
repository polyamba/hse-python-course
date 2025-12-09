import requests
import logging
import os
import time
from typing import List, Dict, Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,           # Минимальный уровень для записи
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщения
    datefmt='%H:%M:%S',           # Формат времени
    filename='app.log',           # Опционально: запись в файл
    filemode='a',                 # Опционально: 'a' для дописывания, 'w' для перезаписи
    encoding='utf-8',             # Опционально: кодировка файла
    force=True                    # Опционально: переопределить существующую конфигурацию
    )
logger = logging.getLogger(__name__)

class IPGeolocation:
    """
    Клиент для определения геолокации по IP через ipapi.co
    
    Документация: https://ipapi.co/api/
    Не требует API ключа для базовых запросов
    Лимит: 1000 запросов в день
    """
    
    def __init__(self):
        self.base_url = "https://ipapi.co"
    
    def get_location(self, ip_address: str) -> Optional[Dict]:
        """Определяет геолокацию по IP адресу"""
        try:
            url = f"{self.base_url}/{ip_address}/json/"
            # Сделать get-запрос 
            # Передать url и таймаут 10
            # Проверить HTTP-ответ, и если 200, то получить данные с API как JSON
            response = requests.get(
                url, 
                timeout = 10
            )                
            if response.status_code == 200:
                data = response.json()     # Проверяем есть ли ошибка в ответе
                if data.get('error'):
                    logger.error(f"Geolocation error: {data.get('reason')}")
                    return None
                
                return {
                    'ip': data.get('ip'),
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('org'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
            else:
                # logger.error выводит ошибку геолокации
                logger.error(f"Geolocation error for IP {ip_address} : HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            # logger.error(f"Network error during geolocation: {e}") выводит сетевую ошибку
            logger.error("{e} during geolocation: Connection error")
            # Пример вывода: "Network error during geolocation: Connection error"
            return None
    
    def get_own_ip_location(self) -> Optional[Dict]:
        """Определяет геолокацию собственного IP адреса"""
        try:
            # Сначала получаем свой внешний IP
            ip_response = requests.get('https://api.ipify.org', timeout=5)
            own_ip = ip_response.text.strip()
            # logger.info выводит обнаруженный IP
            logger.info(f"Detected own IP: {own_ip}")
            # Пример вывода: "Detected own IP: 192.168.1.100"
            return self.get_location(own_ip)
        except requests.exceptions.RequestException as e:
            # logger.error выводит ошибку определения IP
            logger.error("Error detecting own IP: Failed to resolve 'api.ipify.org'")
            # Пример вывода: "Error detecting own IP: Failed to resolve 'api.ipify.org'"
            return None



# Демонстрация работы всех клиентов
if __name__ == "__main__":    
    # logger.info выводит заголовок теста
    logger.info("Testing IP Geolocation...")
    # Пример вывода: "Testing IP Geolocation..."
    geo = IPGeolocation()
    
    # Тестируем несколько IP адресов
    test_ips = ['8.8.8.8', '1.1.1.1', '23.94.48.109']
    for ip in test_ips:
        location = geo.get_location(ip)
        if location:
            # logger.info выводит информацию о геолокации
            logger.info(f"IP {ip}: {location['country']}, {location['region']}, {location['city']} (Google LLC)")
            # Пример вывода: "IP 8.8.8.8: Mountain View, United States (Google LLC)"
    
    # Определяем свою геолокацию
    own_location = geo.get_own_ip_location()
    if own_location:
        # logger.info выводит местоположение пользователя
        logger.info(f"Your location: {own_location['city']}, {own_location['country']}")
        # Пример вывода: "Your location: Moscow, Russia"
