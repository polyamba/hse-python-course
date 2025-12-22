import tempfile
import os
import json

"""
TemporaryDirectory - временная директория для работы с временными файлами
"""

# Пример 1: Создание временных конфигов для бота
def setup_bot_environment(configs):
    """Создает временные конфигурационные файлы для бота"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(configs, f, indent=2)
        tokens_path = os.path.join(temp_dir, 'tokens.json')
        with open(tokens_path,  'w') as f:
            f.write(configs.get('main')['token'])
        webhook_path = os.path.join(temp_dir, 'webhook.txt')
        with open(webhook_path, 'w') as f:
            f.write(configs.get('main')['webhook'])
        files = os.listdir(temp_dir)  
        print("Файлы:", files)
        
        print(f"Пример 1 - Временная директория: {temp_dir}")
        

# Пример 2: Обработка временных медиа-файлов
def process_user_media(user_id, media_data):
    """Обрабатывает временные медиа-файлы пользователя"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = os.path.join(temp_dir, f"user_{user_id}")
        os.makedirs(user_dir)
        avatar_path = os.path.join(user_dir, 'avatar.jpg')
        with open(avatar_path, 'w') as f:
            f.write(media_data[0])
        media_paths = []
        for i, data in enumerate(media_data[1:], 1):
            media_path = os.path.join(user_dir, f'media_{i}.jpg')
            with open(media_path, 'w') as f:
                f.write(data)
            media_paths.append(media_path)
        files = os.listdir(user_dir)
        print("Файлы пользователя:", files)
        
        print(f"Пример 2 - Обработка медиа для пользователя {user_id}")

# # Пример 3: Временное кэширование данных бота
def cache_bot_data(cache_data):
    """Создает временный кэш данных бота"""

    with tempfile.TemporaryDirectory() as temp_dir:
        users_cache_path = os.path.join(temp_dir, 'users_cache.json')
        with open(users_cache_path, 'w') as f:
            json.dump(cache_data.get('users', {}), f, indent=2)
        messages_cache_path = os.path.join(temp_dir, 'messages_cache.json')
        with open(messages_cache_path, 'w') as f:
            json.dump(cache_data.get('messages', []), f, indent=2)
        state_cache_path = os.path.join(temp_dir, 'state_cache.json')
        with open(state_cache_path, 'w') as f:
            json.dump(cache_data.get('state', {}), f, indent=2)
        files = os.listdir(temp_dir)
        print("Файлы кэша:", files)
        
        print("Пример 3 - Кэширование данных бота")
        

# # Пример 4: Создание временных логов
def create_temporary_logs(log_entries):
    """Создает временные лог-файлы для отладки"""

    with tempfile.TemporaryDirectory() as temp_dir:
        debug_log_path = os.path.join(temp_dir, 'debug.log')
        with open(debug_log_path, 'w') as f:
            f.write('\n'.join(log_entries))
        errors_log_path = os.path.join(temp_dir, 'errors.log')
        with open(errors_log_path, 'w') as f:
            errors = [entry for entry in log_entries if entry.startswith('ERROR')]
            f.write('\n'.join(errors))
        actions_log_path = os.path.join(temp_dir, 'actions.log')
        with open(actions_log_path, 'w') as f:
            actions = [entry for entry in log_entries if entry.startswith('ACTION')]
            f.write('\n'.join(actions))
        files = os.listdir(temp_dir)
        print("Файлы логов:", files)
        
        print("Пример 4 - Временные логи для отладки")
        

if __name__ == "__main__":
    # Пример с конфигами бота
    bot_configs = {
        "main": {"token": "abc123", "webhook": "https://bot.com"},
        "database": {"host": "localhost", "port": 5432}
    }
    setup_bot_environment(bot_configs)
    
    # Пример с медиа-файлами
    media_data = ["avatar_data", "photo_1", "photo_2"]
    process_user_media(12345, media_data)
    
    # Пример с кэшированием
    cache_data = {
        "users": {"user1": "active", "user2": "inactive"},
        "messages": ["msg1", "msg2", "msg3"]
    }
    cache_bot_data(cache_data)
    
    # Пример с логами
    logs = [
        "DEBUG: Bot started",
        "ERROR: Connection failed", 
        "ACTION: User clicked button"
    ]
    create_temporary_logs(logs)