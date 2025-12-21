from solution import TextDataLoader

def test_extract_posts_comprehensive():
    """Комплексное тестирование extract_posts с assert"""
    
    
    # Тестовые данные
    sample_data = {
        "name": "Test",
        "messages": [
            {"id": 1, "date": "2023-06-03T23:52:37", "text": "Post 1", "other_field": "value"},
            {"id": 2, "date": "2023-06-03T23:52:37", "text": "Post 2"}
        ]
    }

    loader = TextDataLoader(sample_data)
    result = loader.extract_posts()

    assert isinstance(result, list), "Результат должен быть списком"
    assert len(result)==2, "Должно быть извлечено 2 поста"
    assert result[0].get('text') == 'Post 1', "Первый пост должен быть 'Post 1'"
    assert result[1].get('text') == 'Post 2', "Второй пост должен быть 'Post 2'"
    assert all(type(n)==str for n in [r['text'] for r in result]), "Все элементы должны быть строками" 
    print('Все проверки пройдены успешно.')

test_extract_posts_comprehensive()
