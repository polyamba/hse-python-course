import re

def clean_text(data):
    """Очищает тексты постов"""
    text = "" if data is None else str(data)

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

if __name__ == "__main__":
    pass