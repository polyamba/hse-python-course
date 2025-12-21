from solution_2 import TextDataLoader

"""
Перепишите тесты для методов clean_text и extract_posts используя:

- Assert с сообщениями об ошибках (2 любых теста)
- Множественные проверки в одном assert (2 любых теста)
- Создайте кастомную функцию, которая проверяет 2 теста сразу
"""
loader = TextDataLoader()
cleaned = loader.clean_text()
extracted = loader.extract_posts()

assert all("  " not in t["text"] for t in cleaned), "В тексте не должно быть двойных пробелов"
assert [r['id'] for r in extracted] == list(range(1, len(extracted) + 1)), "Идентификаторы постов должны быть последовательными числами от 1 до N"

assert all('\n' not in t['text'] for t in cleaned) and all(t['text'] == t['text'].lower() for t in cleaned), "Все тексты должны быть в нижнем регистре и не содержать символов новой строки"
assert all(len(r['text']) > 0 for r in extracted) and all(isinstance(r['text'], str) for r in extracted), "Все тексты постов должны быть непустыми строками и соответсовать типу str"

def total_check(cleaned, extracted):
    """Кастомная функция проверки очистки текста и извлечения постов"""
    assert all(len(t['text'])==len(t['text'].strip()) for t in cleaned), "Тексты не должны содержать пробелов по краям"
    assert all('id' in r and 'date' in r and 'text' in r for r in extracted), "Каждый пост должен содержать поля 'id', 'date' и 'text'"
