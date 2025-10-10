import os 
import pandas as pd

class DataLoader():

    def __init__(self, file_path):
        self.data = self.load_data(file_path)

    def _validate_file_path(self, file_path):
        """
        Проверяет, что файл существует, является файлом и имеет расширение .csv.
        Возвращает путь, если всё корректно.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не найден.")
        
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Путь '{file_path}' не является файлом.")
        
        if not file_path.lower().endswith('.csv'):
            raise ValueError(f"Файл '{file_path}' должен иметь расширение .csv.")
        
        return file_path
    
    def load_data(self, file_path):
        """
        Загружает CSV-данные из файла
        """
        self._validate_file_path(file_path)
        df = pd.read_csv(file_path)
        return df
    
    def get_basic_info(self):
        """
        Выводит базовую информацию о датасете: размер, 
        названия колонок и количество пропущенных значений в каждой колонке.
        """
        shape = self.data.shape
        column_names = self.data.columns.values
        missing_values = self.data.isnull().sum()
        return f'Размер датасета: {shape}\nНазвания колонок: {column_names}\nПропуски в данных:\n{missing_values}'



if __name__=="__main__":
    loader = DataLoader('path_to_data.csv')
    print(loader.data.head())
    info = loader.get_basic_info()
    print(info)
