import tempfile
import json

"""
TemporaryFile - анонимный временный файл для безопасной работы с конфиденциальными данными
"""

# Пример 1: Безопасная работа с API ключами в боте
def process_sensitive_data(api_key, secret_token):
    """Обрабатывает конфиденциальные данные во временном файле"""
    
    with tempfile.TemporaryFile(mode='w+') as temp_file:
        credentials = {
            'api_key': api_key,
            'secret_token': secret_token
        }
        json.dump(credentials, temp_file)
        temp_file.seek(0)
        data = json.load(temp_file)
        return data['api_key'][:8]


# Пример 2: Временное хранение токена авторизации
def handle_user_session(user_token):
    """Работа с токеном пользователя во временном файле"""
    
    with tempfile.TemporaryFile(mode='w+') as temp_file:
        temp_file.write(user_token)
        temp_file.seek(0)
        token = temp_file.read()
        print(f'Токен пользователя: {token[:10]}')
        temp_file.seek(0)
        temp_file.truncate()
        temp_file.write(user_token + "_refreshed")
        temp_file.seek(0)
        return temp_file.read()

# Пример 3: Обработка временных конфигураций бота
def load_bot_configuration(config_data):
    """Загружает конфигурацию бота во временный файл"""
    
    with tempfile.TemporaryFile(mode='w+') as temp_file:
        temp_file.write(json.dumps(config_data, indent=2))
        temp_file.seek(0)
        config = json.load(temp_file)
        return list(config.keys())

# Демонстрация использования
if __name__ == "__main__":
    print(process_sensitive_data("sk-1234567890abcdef", "supersecrettoken123"))
    
    # Пример с токеном пользователя
    print(handle_user_session("user_auth_token_xyz_987654"))
    
    # Пример с конфигурацией бота
    bot_config = {
        "api_key": "telegram_bot_key",
        "webhook_url": "https://example.com/webhook",
        "admin_ids": [12345, 67890]
    }
    print(load_bot_configuration(bot_config))