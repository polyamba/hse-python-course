import requests
import logging
import os
import time
from typing import List, Dict, Optional
from dotenv import dotenv_values

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

class YouTubeSearch:
    """
    Клиент для поиска видео через YouTube Data API
    
    Документация: https://developers.google.com/youtube/v3/docs/search/list
    Получить API ключ: https://console.cloud.google.com/apis/library/youtube.googleapis.com
    Бесплатный тариф: 10000 запросов в день
    """
    
    def __init__(self):
        self.api_key = dotenv_values(".env")['API_YOUTUBE']
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
    
    def search_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """Ищет видео на YouTube по запросу"""
        if not self.api_key:
            logger.error("YOUTUBE_API_KEY not found in .env file")
            logger.info("Get API key from: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
            return []
        
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': min(max_results, 10),
                'key': self.api_key
            }
            r = requests.get(
                self.base_url,
                params,
                timeout=15
            )

            if r.status_code == 200:
                data = r.json()
                videos = []
                
                for item in data.get('items', []):
                    video_data = {
                        'title': item['snippet']['title'],
                        'video_id': item['id']['videoId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'description': item['snippet']['description'][:100] + '...' if item['snippet']['description'] else '',
                        'url': f"https://youtube.com/watch?v={item['id']['videoId']}"
                    }
                    videos.append(video_data)
                
                logger.info(f"Found {max_results} videos for query '{query}'")
                return videos
                
            elif r.status_code == 403:
                logger.error("YouTube API authentication error or quota exceeded")
                return []
            else:
                logger.error("YouTube API error: 400")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error("Network error during video search: SSL certificate verify failed")
            return []



if __name__ == "__main__":    
    logger.info("Testing YouTube Search...")
    youtube = YouTubeSearch()
    if youtube.api_key:
        videos = youtube.search_videos("python tutorials", max_results=3)
        for video in videos:
            logger.info(f"{video['title']}")
    else:
        logger.warning("YouTube API key not configured")
