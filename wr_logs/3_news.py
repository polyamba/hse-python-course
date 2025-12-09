import requests
import logging
import os
import time
from typing import List, Dict
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,          
    format='%(asctime)s - %(levelname)s - %(message)s',  
    datefmt='%H:%M:%S',         
    filename='app.log',          
    filemode='a',              
    encoding='utf-8',            
    force=True                    
    )
logger = logging.getLogger(__name__)
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
            logger.error("NEWS_API_KEY not found in .env file")
            logger.info("Get free API key from: https://newsapi.org/register")
            return []
        
        try:
            params = {
                'q': topic,
                'pageSize': min(max_results, 10),
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(
                self.base_url,
                params,
                timeout=15
            )             
            
            if response.status_code == 200:
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
                
                logger.info(f"Found {max_results} news articles for topic {topic}")
                return news_list
                
            elif response.status_code == 401:
                logger.error("Invalid NewsAPI key")
                return []
            elif response.status_code == 429:
                logger.warning("NewsAPI rate limit exceeded")
                return []
            else:
                logger.error("NewsAPI error: 500")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error("{e} during news request: Read timed out")
            return []


if __name__ == "__main__":    
    logger.info("Testing News API...")
    news = NewsAPIClient()
    if news.api_key:
        python_news = news.get_news("python programming", max_results=3)
        for article in python_news:
            logger.info(f"News: {article['title']}")
            time.sleep(3)
    else:
        logger.warning("NewsAPI key not configured")
