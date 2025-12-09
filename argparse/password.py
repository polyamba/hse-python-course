import argparse
import string
import random

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--length',
                   type = int, 
                   default = 8, 
                   help = 'lenth of the password')
parser.add_argument('-u', '--uppercase',
                    action = 'store_true',
                    help = 'include uppercase leyyers in the password') 
parser.add_argument('-d', '--digits', 
                    action = 'store_true', 
                    help = 'include digits in the password')
parser.add_argument('-s', '--symbols', 
                    action = 'store_true', 
                    help = 'include symbols in the password')

args = parser.parse_args()

character_string = ''
character_string += string.ascii_lowercase

if args.uppercase:
    character_string += string.ascii_uppercase
if args.digits:
    character_string += string.digits
if args.symbols:
    character_string += string.punctuation

password = ''.join(random.choice(character_string) for _ in range(args.length))
print(f'Generated password: {password}')
