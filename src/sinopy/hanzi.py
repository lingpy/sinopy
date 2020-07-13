"""
Utilities for operations with Chinese characters
"""
from sinopy.data import *
from sinopy.util import is_chinese
from lingpy.sequence.ngrams import get_all_ngrams
from lingpy.sequence.ngrams import trigrams
from sinopy.util import is_chinese

ids = get_ids()
idsr = {v: k for k, v in ids.items()}
helper = lambda x: len(x) == 1 and ord(x[0]) in range(12250, 12300)

def compose(chars, ids=ids, _return_list=False):
    """
    Find the complex character for character components.
    """
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
    """
    Split a character into its components.
    """
    
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


def character_from_structure(motivation):
    """
    Find a character for a given structure.
    
    Note
    ----
    This is a utility function that makes it easier to parse the more complex
    motivation structures that are handled by compose and decompose.
    """
    assert len(motivation) == 3

    _c = {
            "+": "⿰",
            "-": "⿱",
            '>': "⿱",
            "手": "扌",
            "人": "亻",
            "刀": "刂",
            "丝": "糹",
            "水": "氵",
            "0": "⿴",
            }
    structure = ''.join([_c.get(x, x) for x in motivation])
    return IDS.get(structure, '?')

def gbk2big5(chars):
    """
    Convert from gbk format to big5 representation of chars.
    """
    out = ''
    for char in chars:
        if char in GBK:
            out += BIG5[GBK.index(char)]
        else:
            out += char
    return out

def pinyin(char, variant='mandarin', sep=' ', out='tones'):
    """
    Retrieve Pinyin of a character.
    """
    if len(char) > 1:
        return sep.join([pinyin(c, variant=variant, sep=sep, out=out) for c in char])

    if not is_chinese(char):
        return char

    if char in GBK: 
        char = gbk2big5(char)

    out_char = UNIHAN.get(char, {variant: '?({0}'.format(char)}).get(variant, '!({0})'.format(char))

    if out != 'tones':
        out_char = ''.join([tone_converter.get(x, x) for x in out_char])    

    return out_char


def chars2baxter(chars):
    """
    Convert a sequence of Characters to their MCH values.
    """

    out = []
    chars = gbk2big5(chars)

    for char in chars:
        tmp = []
        if char in TLS:
            for entry in TLS[char]:
                baxter = TLS[char][entry]['BAXTER']
                if baxter != '?':
                    tmp += [baxter]
        out += [','.join(tmp)]
    return out


def big52gbk(chars):
    """
    Convert from long chars to short chars.
    """
    out = ''
    for char in chars:
        if char in BIG5:
            out += GBK[BIG5.index(char)]
        else:
            out += char
    return out


def chars2gloss(chars):
    """
    Get the TLS basic gloss for a characters.
    """
    out = []
    chars = gbk2big5(chars)
    for char in chars:
        tmp = []
        if char in TLS:
            for entry in TLS[char]:
                baxter = TLS[char][entry]['UNIHAN_GLOSS']
                if baxter != '?':
                    tmp += [baxter]
        out += [','.join(tmp)]
    return out
