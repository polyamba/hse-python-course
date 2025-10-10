import json

class Dataset:
    def __init__(self, filename:str):
        self.filename = filename
        self.data = self._read_file()
        self.song_dict = {song['id']: [song['title'], song['similar_ids']] for song in self.data} if self.data else {}

    def _read_file(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: The file 'data.json' was not found.")
        except Exception as e:
            print(f'Ошибка: {e}')

    def get_song(self, n:int):
        return self.song_dict.get(n)[0]  
            
    def find_similar(self, n:int):
        similar_songs = self.song_dict.get(n)[1]
        for i in similar_songs:
            print(self.song_dict.get(i)[0])
                    
if __name__ == '__main__':
    dataset = Dataset('/Users/polyamba/Desktop/питон/api.json')
    print(dataset.data[:5])
    print(dataset.get_song(3))
    dataset.find_similar(3)