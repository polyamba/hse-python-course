# Задача: Создать скрипт для подсчета слов/символов в файле
# Использование: 
#   python wordcount.py text.txt --words
#   python wordcount.py text.txt --chars --lines
# Опции: --words, --chars, --lines (можно комбинировать)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('txt_file',
                    type = str, 
                    help='path to the text file for counting') 
parser.add_argument('-w', '--words',
                    action = 'store_true',
                    help='counts words in the file') 
parser.add_argument('-c', '--chars',
                    action = 'store_true',
                    help='counts chars in the file') 
parser.add_argument('-l', '--lines',
                    action = 'store_true',
                    help='counts lines in the file') 

args = parser.parse_args()

f = open(args.txt_file, 'r', encoding='utf-8')
text = f.read()
if text:
    if args.words:
        counter = text.split()
        print(f'Words: {len(counter)}')
    if args.chars:
        print(f'Chars: {len(text)}')
    if args.lines:
        print(f'Lines: {len(text.splitlines())}')
