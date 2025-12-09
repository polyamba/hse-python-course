import requests
import logging
import os
import time
from typing import List, Dict
from dotenv import load_dotenv

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
### ваш код здесь ###
load_dotenv()

class NewsAPIClient:
    """
    Клиент для получения новостей через NewsAPI
    
    Документация: https://newsapi.org/docs
    Получить API ключ: https://newsapi.org/register
    Бесплатный тариф: 100 запросов в день
    """

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
    
    def get_news(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Получает новости по заданной теме"""
        if not self.api_key:
            # logger.error выводит ошибку отсутствия API ключа
            logger.error("NEWS_API_KEY not found in .env file")
            # Пример вывода: "NEWS_API_KEY not found in .env file"
            # logger.info выводит подсказку где взять ключ
            logger.info("Get free API key from: https://newsapi.org/register")
            # Пример вывода: "Get free API key from: https://newsapi.org/register"
            return []
        
        try:
            params = {
                'q': topic,
                'pageSize': min(max_results, 10),
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            
            # Сделать get-запрос
            # Передать url, параметры и таймаут - 15
            # Проверить HTTP-ответы (на ошибки)
            response = requests.get(
                self.base_url,
                params,
                timeout=15
            )             
            
            if response.status_code == 200:
                # Получаем ответ как JSON
                data = response.json()
                articles = data.get('articles', [])
                
                news_list = []
                for article in articles[:max_results]:
                    news_list.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', '')
                    })
                
                # logger.info выводит количество найденных новостей
                logger.info(f"Found {max_results} news articles for topic {topic}")
                # Пример вывода: "Found 5 news articles for topic 'python programming'"
                return news_list
                
            elif response.status_code == 401:
                # logger.error выводит ошибку невалидного ключа
                logger.error("Invalid NewsAPI key")
                # Пример вывода: "Invalid NewsAPI key"
                return []
            elif response.status_code == 429:
                # logger.warning выводит предупреждение о лимите запросов
                logger.warning("NewsAPI rate limit exceeded")
                # Пример вывода: "NewsAPI rate limit exceeded"
                return []
            else:
                # logger.error выводит ошибку API
                logger.error("NewsAPI error: 500")
                # Пример вывода: "NewsAPI error: 500"
                return []
                
        except requests.exceptions.RequestException as e:
            # logger.error выводит сетевую ошибку
            logger.error("{e} during news request: Read timed out")
            # Пример вывода: "Network error during news request: Read timed out"
            return []


# Демонстрация работы всех клиентов
if __name__ == "__main__":    
    # logger.info выводит заголовок теста
    logger.info("Testing News API...")
    # Пример вывода: "Testing News API..."
    news = NewsAPIClient()
    if news.api_key:
        python_news = news.get_news("python programming", max_results=3)
        for article in python_news:
            # logger.info выводит заголовок новости
            logger.info(f"News: {article['title']}")
            # Пример вывода: "News: Python 3.11 Released with Major Performance Improvements"
            time.sleep(3)
    else:
        # logger.warning выводит предупреждение о ненастроенном ключе
        logger.warning("NewsAPI key not configured")
