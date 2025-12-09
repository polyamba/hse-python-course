import requests
import logging
import os
import time
from typing import List, Dict, Optional

# Настройка логирования
# Базовая конфигурация со всеми опциями
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

class CryptoPriceChecker:
    """
    Клиент для получения цен криптовалют через CoinGecko API
    
    Документация: https://www.coingecko.com/api/documentations/v3
    Не требует API ключа для базовых запросов
    Список криптовалют: https://api.coingecko.com/api/v3/coins/list
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
    
    def get_price(self, crypto_id: str) -> Optional[Dict]:
        """Получает текущую цену криптовалюты по ее ID"""
        try:
            params = {
                'ids': crypto_id,    # ID криптовалюты
                'vs_currencies': 'usd', # Валюта для отображения цены
                'include_24hr_change': 'true'    # Включить изменение цены за 24 часа
            }
            
            ### ваш код здесь ###
            # Задание 2: сделать get-запрос
            # передать в запрос эндпоинт (base url), 
            # параметры запроса (предыдущая строка этой функции)
            # и таймаут = 10
            response = requests.get(
                self.base_url,
                params,
                timeout=10
            )            
            
            # Выполнить проверку кода запроса
            
            if response.status_code == 200:
                data = response.json() # преобразует JSON ответ от API в Python словарь
                crypto_data = data.get(crypto_id)
                
                if crypto_data:
                    return {
                        'name': crypto_id.title(),
                        'current_price': crypto_data.get('usd'),
                        'price_change_24h': crypto_data.get('usd_24h_change'),
                        'currency': 'USD'
                    }
                else:
                    # logger.warning выводит предупреждение о ненайденной крипте
                    logger.warning("Cryptocurrency unknown_coin not found")
                    # Пример вывода: "Cryptocurrency unknown_coin not found"
                    return None
            else:
                # logger.error выводит ошибку API
                logger.error( "CoinGecko API error: 429")
                # Пример вывода: "CoinGecko API error: 429"
                return None
                
        except requests.exceptions.RequestException as e:
            # logger.error выводит сетевую ошибку
            logger.error("Network error during price request: Connection refused")
            # Пример вывода: "Network error during price request: Connection refused"
            return None
    
    def get_multiple_prices(self, crypto_ids: List[str]) -> Dict[str, Optional[Dict]]:
        """Получает цены для нескольких криптовалют одновременно"""
        results = {}
        for crypto_id in crypto_ids:
            results[crypto_id] = self.get_price(crypto_id)
            # Задержка между запросами чтобы избежать лимитов API
            time.sleep(5)
        return results


# Демонстрация работы всех клиентов
if __name__ == "__main__":    
    # logger.info выводит заголовок теста
    logger.info("Testing Cryptocurrency Prices...")
    # Пример вывода: "Testing Cryptocurrency Prices..."
    crypto = CryptoPriceChecker()
    
    # Тестируем несколько криптовалют
    cryptocurrencies = ['bitcoin', 'ethereum', 'cardano', 'solana', 'dogecoin']
    prices = crypto.get_multiple_prices(cryptocurrencies)
    
    for crypto_id, price_data in prices.items():
        if price_data:
            change = price_data['price_change_24h'] or 0
            change_symbol = "+" if change > 0 else ""
            # logger.info выводит цену крипты с изменением
            logger.info(f"bitcoin: {price_data['current_price']} ({change_symbol}{round(change*100, 2)}%)")
            # Пример вывода: "bitcoin: $45000.50 (+2.35%)"
    
    # logger.info выводит заголовок теста
    ### ваш код здесь ###
    logger.info("Stop")
