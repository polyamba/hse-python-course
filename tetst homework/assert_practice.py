from cleaning import clean_text

def test_clean_text_with_assert():
    """Тестирование clean_text с использованием assert"""    
    # Тест очистки пробелов
    result = clean_text("  Hello  World  ")
    assert result == "hello world", "Должны удаляться лишние пробелы"
    
    # Тест нижнего регистра
    result = clean_text("HELLO")
    assert result == "hello", "Текст должен быть в нижнем регистре"
    
    # Тест специальных символов
    result = clean_text("Hello! @user #tag")
    assert "!" not in result, "Должны удаляться специальные символы"
    assert "@" not in result, "Должны удаляться @ символы"
    # 4. Напишите еще один тест для проверки удаления хештегов и знаков препинания
    assert "#" not in result, "Должны удаляться # символы"
    assert '.' not in result, "Должны удаляться точки"
    assert ',' not in result, "Должны удаляться запятые"
    assert ';' not in result, "Должны удаляться точки с запятой"
    assert ':' not in result, "Должны удаляться двоеточия"
    assert '!' not in result, "Должны удаляться восклицательные знаки"
    assert '?' not in result, "Должны удаляться вопросительные знаки"
    assert '%' not in result, "Должны удаляться проценты"
    assert '-' not in result, "Должны удаляться дефисы"

    # 5. Проверьте, что пустые строки никак не обрабатываются методом clean_text
    result = clean_text('')
    assert result == '', "Пустые строки не должны изменяться"

    # 6. Убедитесь в том, что нестроковые данные преобразовываются к виду строк 
    result = clean_text(1234)
    assert isinstance(result, str), "Нестроковые данные должны преобразовываются к виду строк"

test_clean_text_with_assert()


