import requests
import logging
import os
import time
from typing import List, Dict, Optional

import logging

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

class URLShortener:
    """
    Клиент для сервиса сокращения ссылок CleanURI
    
    Документация API: https://cleanuri.com/docs
    Не требует API ключа
    """
    
    def __init__(self):
        self.base_url = "https://cleanuri.com/api/v1/shorten"
    
    def shorten_url(self, long_url: str) -> Optional[str]:
        """Сокращает URL через cleanuri.com API"""
        try:
            response = requests.post(
                self.base_url,
                data={'url': long_url},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                short_url = data.get('result_url')
                logger.info(f"URL shortened: {long_url} -> {short_url}")
                return short_url
            else:
                logger.error("URL shortening error: 400 - Invalid URL")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error("Network error during URL shortening: Connection timed out")
            return None

if __name__ == "__main__":
    logger.info("Testing URL Shortener...")
    shortener = URLShortener()
    short_url = shortener.shorten_url("https://www.python.org/downloads/")
    if short_url:
        logger.info(f"Short URL: {short_url}")
