

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('path',
                    type = str, 
                    help='path to the directory for searching files') 
parser.add_argument('--ext', 
                    nargs='+',
                    help = 'file extensions to search for (e.g., txt, pdf)')

args = parser.parse_args()
for e in args.ext:
    for p in Path(args.path).rglob(pattern = f'*.{e}'):
        if p is not None:
            print(p)
