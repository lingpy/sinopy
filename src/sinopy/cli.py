from sys import argv
from sinopy import sinopy, segments
from lingpy import Wordlist

def main():
    
    debug=False
    if 'debug' in argv:
        debug=True
    if 'pinyin' in argv:
        py = sinopy.pinyin(argv[argv.index('pinyin')+1])
        print(py)
    if 'profile' in argv:
        wl = Wordlist(argv[argv.index('profile')+1])
        column = 'ipa'
        language = None
        filename = 'orthography.tsv'
        if '--column' in argv:
            column = argv[argv.index('--column')+1]
        if '--language' in argv:
            language = argv[argv.index('--language')+1]
        if '-l' in argv: 
            language = argv[argv.index('-l')+1]
        if '-o' in argv:
            filename = argv[argv.index('-o')+1]
        if '--filename' in argv:
            filename = argv[argv.index('--filename')+1]

        segments.write_structure_profile(wl, column=column,
                filename=filename, debug=debug, language=language)
