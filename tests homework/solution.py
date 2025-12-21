import os
import json
import re
import pandas as pd

class TextDataLoader():
    def __init__(self, file_path:str):
        self.data = self.load_data(file_path)
        self.posts = self.extract_posts()
        self.cleaned_posts = self.clean_text()
    
    def _validate_file_path(self, file_path):
        """Проверяет, что файл существует, является файлом и имеет расширение .json"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не существует")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"'{file_path}' является директорией, а не файлом")
        if not file_path.endswith('.json'):
            raise ValueError(f"Ошибка расширения файла '{file_path}'")
    
    def load_data(self, file_path:str):
        """Загружает JSON-данные из файла после проверки пути"""
        self._validate_file_path(file_path)
        try:
            with open(file_path, 'r', encoding = 'utf-8') as file:
                return json.load(file)
        except json.decoder.JSONDecodeError as e:
            print(f'Ошибка декодирования файла {e}')
        except Exception as e:
            print(f'Ошибка: {e}')
        
    def extract_posts(self):
        """Извлекает тексты постов"""
        posts = []

        if not isinstance(self.data, dict):
            return posts

        for message in self.data.get('messages', []):
            text = message.get('text')

            if isinstance(text, str):
                text = text.strip()
            elif isinstance(text, list):
                text = ' '.join(part for part in text if isinstance(part, str)).strip()
            else:
                continue

            if not text:
                continue

            posts.append({
                'id': len(posts) + 1,
                'date': message.get('date', '')[:10],
                'text': text
            })

        return posts  
    
    def clean_text(self):
        """Очищает тексты постов"""
        for post in self.posts:
            text = post.get('text')
            cleaned_text = re.sub(r'[^\w\s]', '', text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            post['text'] = cleaned_text.strip().lower()
    
        return self.posts
    
    def save_to_csv(self, output_file:str = 'telegram.csv'):
        """Сохраняет очищенные тексты в CSV-файл"""
        df = pd.DataFrame(self.cleaned_posts)
        df = df.dropna()
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f'Данные сохранены в файл {output_file}')
        return output_file
    

if __name__=="__main__":
    loader = TextDataLoader('/Users/polyamba/Desktop/домашки/homework (tetst)/result.json')
    loader.load_data('/Users/polyamba/Desktop/домашки/homework (tetst)/result.json')
    loader.save_to_csv()
    # print(loader.extract_posts()[:10])

