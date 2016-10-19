from sys import argv
from sinopy import sinopy

def main():
    
    if 'pinyin' in argv:
        py = sinopy.pinyin(argv[argv.index('pinyin')+1])
        print(py)
