from sinopy.data import *
from sinopy.sinopy import is_chinese
from lingpy.sequence.ngrams import get_all_ngrams
from lingpy.sequence.ngrams import trigrams

ids = get_ids()
idsr = {v: k for k, v in ids.items()}
helper = lambda x: len(x) == 1 and ord(x[0]) in range(12250, 12300)

def compose(chars, ids=ids, _return_list=False):
    # test: ⿰亻⿱立日 -> 偣 
    # replace triples by their counterparts
    #triples = [
    #        ('⿳', '⿱⿱'),
    #        ]
    #for s, t in triples:
    #    chars = chars.replace(s, t)
    # search for xAB pairs
    while True:
        found = False
        if len(chars) > 1:
            for i, grams in enumerate(
                    sorted(
                        get_all_ngrams(chars), 
                        key=lambda x: len(x),
                        reverse=True
                        )
                    ):
                if helper(grams[0]) and grams in ids and len(grams) > 1:
                    idx = chars.index(grams)
                    chars = chars[:idx]+ids[grams]+chars[idx+len(grams):]
                    found = True
                    break
            if not found:
                return '?'+chars
        else:
            break
    return chars

def decompose(character, ids=idsr, _return_list=False, depth=2):
    
    chars = [(character, 0)]
    out = ''
    if depth == 0:
        return character

    while chars:
        charls, d = chars.pop(0)
        nchars = []
        for char in charls:
            if helper(char):
                nchars += ['--'+char]
            elif char in ids and ids[char] != char:
                nchars += list(ids[char])
            else:
                nchars += ['--'+char]
        if d < depth and [x for x in nchars if not x.startswith('--')]:
            chars += [(nchars, d+1)]
    return ''.join([x.lstrip('-') for x in nchars])


