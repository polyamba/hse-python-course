# Задача: Создать скрипт, который принимает два числа и операцию
# Использование: python calc.py 10 5 --operation add
# Должен поддерживать: add, subtract, multiply, divide
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('num_1',
                    type = int, 
                    help='first number for math operation') 
parser.add_argument('num_2',
                    type = int, 
                    help='second number for math operation') 
parser.add_argument('--operation',
                    type = str, 
                    help='math operations that can be used: add, subtract, multiply, divide', 
                    choices=['add', 'subtract', 'multiply', 'divide']) 

args = parser.parse_args()

if args.operation == 'add':
    print(args.num_1 + args.num_2)
elif args.operation == 'subtract':
    print(args.num_1 - args.num_2)
elif args.operation == 'multiply':
    print(args.num_1 * args.num_2)
elif args.operation == 'divide':
    print(args.num_1 / args.num_2)
    



