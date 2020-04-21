"""
Operations on data from South-East-Asian languages
"""
import lingpy
from lingpy.sequence import sound_classes as lsc
from clldutils.text import strip_chars

def parse_chinese_morphemes(
        seq, 
        context=False,
        model=False
        ):
    """
    Parse a Chinese syllable and return its basic structure.

    """

    if not model:
        model = lingpy.rc('art')
    
    # get the tokens
    if isinstance(seq, list):
        tokens = [s for s in seq]
    else:
        tokens = lingpy.ipa2tokens(seq, merge_vowels=False)
    
    # get the sound classes according to the art-model
    arts = [int(x) for x in lingpy.tokens2class(tokens, model, cldf=True)]

    # get the pro-string
    prostring = lingpy.prosodic_string(arts, cldf=True)

    # parse the zip of tokens and arts
    I,M,N,C,T = '','','','',''
    
    ini = False
    med = False
    nuc = False
    cod = False
    ton = False
    
    triples = [('?','?','?')]+list(zip(
        tokens, arts, prostring))+[('?','?','?')]

    for i in range(1,len(triples)-1): 
        t, c, p = triples[i]
        _t, _c, _p = triples[i-1]
        t_, c_, p_ = triples[i+1]

        # check for initial entry first
        if p == 'A' and _t == '?':
            # now, if we have a j-sound and a vowel follows, we go directly to
            # medial environment
            if t[0] in 'jɥw':
                med = True
                ini,nuc,cod,ton = False,False,False,False
            else:
                ini = True
                med,nuc,doc,ton = False,False,False,False
        
        # check for initial vowel
        elif p == 'X' and _t == '?':
            if t[0] in 'iuy' and c_ == '7':
                med = True
                ini, nuc, cod, ton = False,False,False,False
            else:
                nuc = True
                ini, med, cod, ton = False,False,False,False

        # check for medial after initial
        elif p == 'C':
            med = True
            ini, nuc, cod, ton = False,False,False,False

        # check for vowel medial 
        elif p == 'X' and p_ == 'Y':
            
            # if we have a medial vowel, we classify it as medial
            if t in 'iyu':
                med = True
                ini, nuc, cod, ton = False,False,False,False
            else:
                nuc = True
                ini, med, cod, ton = False,False,False,False

        # check for vowel without medial
        elif p == 'X' or p == 'Y':
            if p_ in 'LTY' or p_ == '?':
                nuc = True
                ini, med, cod, ton = False,False,False,False
            elif p == 'Y':
                nuc = True
                ini, med, cod, ton = 4 * [False]
            else:
                cod = True
                ini, med, nuc, ton = 4 * [False]
        
        # check for consonant
        elif p == 'L':
            cod = True
            ini, med, nuc, ton = 4 * [False]

        # check for tone
        elif p == 'T':
            ton = True
            ini, med, nuc, cod = 4 * [False]

        if ini:
            I += t
        elif med:
            M += t
        elif nuc:
            N += t
        elif cod:
            C += t
        else:
            T += t
    
    # bad conversion for output, but makes what it is supposed to do
    out = [I,M,N,C,T]
    tf = lambda x: x if x else '-'
    out = [tf(x) for x in out]
    
    # transform tones to normal letters
    tones = dict(zip('¹²³⁴⁵⁶⁷⁸⁹⁰₁₂₃₄₅₆₇₈₉₀', '1234567890123456789'))

    # now, if context is wanted, we'll yield that
    ic = '1' if [x for x in I if x in 'bdgmnŋȵɳɴ'] else '0'
    mc = '1' if [m for m in M+N if m in 'ijyɥ'] else '0'
    cc = '1' if C in 'ptkʔ' else '0'
    tc = ''.join([tones.get(x, x) for x in T])

    IC = '/'.join(['I',ic, mc, cc, tc]) if I else ''
    MC = '/'.join(['M',ic, mc, cc, tc]) if M else ''
    NC = '/'.join(['N',ic, mc, cc, tc]) if N else ''
    CC = '/'.join(['C',ic, mc, cc, tc]) if C else ''
    TC = '/'.join(['T',ic, mc, cc, tc]) if T else ''

    if context:
        return out, [x for x in [IC, MC, NC, CC, TC] if x]
    return out


def get_structure(
        word, 
        sep='+', 
        zipped=False, 
        semi_diacritics='hsʃʂʒʐzθɕʑfvθðnmȵ'
        ):
    if not isinstance(word, (list, tuple)):
        word = lingpy.ipa2tokens(
                word, 
                expand_nasals=True, 
                merge_vowels=False,
                semi_diacritics=semi_diacritics
                )

    # check for unknown chars
    try: 
        lingpy.tokens2class(word, 'cv', cldf=True)
    except ValueError:
        print('problem with {0}'.format(''.join(word)))
        return []

    # get the morphemes
    if sep in word:
        words = lsc.tokens2morphemes(word, cldf=True)
        morphemes = []
        for w in words:
            morphemes += lsc.tokens2morphemes(w, sep=sep)
    else:
        morphemes = lsc.tokens2morphemes(word, cldf=True)
    # get the basic structure for each morpheme
    for morpheme in morphemes:
        try:
            segments = parse_chinese_morphemes(morpheme)
        except:
            if not zipped:
                yield ['NULL']
            else:
                yield ([('NULL', 'NULL')], morpheme)
        if not zipped:
            yield [x for x, y in zip('imnct', segments) if y != '-']
        else:
            yield ([x for x in zip('imnct', segments) if x[1] != '-'],
                    morpheme)


def get_structure_profile(
        wordlist, 
        column='ipa', 
        text=False,
        semi_diacritics='hsʃʂʒʐzθɕʑfvθð', 
        debug=False, 
        language=None
        ):
    profile = defaultdict(list)
    modify = lambda x: x
    if column == 'ipa':
        modify = lambda x: x.replace(' ', '_')
    
    for idx, lang, segments in lingpy.iter_rows(
            wordlist, 'doculect', column):
        if debug: print(idx, lang, segments)
        if not language or language == lang:
            for structure, morpheme in get_structure(
                    modify(segments), zipped=True, 
                    semi_diacritics=semi_diacritics):
                im, nc, t = [[], []], [[], []], [[], []]
                for pos, seg in structure:
                    if pos in 'i':
                        im[0] += [pos]
                        im[1] += [seg]
                    elif pos in 'mnc':
                        nc[0] += [pos]
                        nc[1] += [seg]
                    else:
                        t[0] += [pos]
                        t[1] += [seg]
                if im[0]:
                    profile[' '.join(im[0]), ' '.join(im[1])] += [(lang,
                        morpheme)]
                if nc[0]:
                    profile[' '.join(nc[0]), ' '.join(nc[1])] += [(lang,
                        morpheme)]
                if t[0]:
                    profile[' '.join(t[0]), ' '.join(t[1])] += [(lang,
                        morpheme)]
    for (pos, seg), langs_ in sorted(profile.items(), key=lambda x: (x[0][0],
        len(x[1])),
            reverse=True):
        langs = [x[0] for x in langs_]
        examples = [''.join(x[1]) for x in langs_]
        if not text:
            yield (seg.replace(' ', ''), seg, seg, pos, codepoint(s), len(langs),
                    ','.join(sorted(set(langs),
                        key=lambda x: langs.count(x))),
                    ', '.join(examples[:5]))
        else:
            yield '\t'.join([
                strip_chars(' ∼', seg), seg, seg, pos, codepoint(seg), str(len(langs)),
                ','.join(sorted(set(langs), key=lambda x: langs.count(x))),
                ', '.join(examples[:5])])
            

def write_structure_profile(wordlist, column='ipa',
        language=None,
        filename='orthography.tsv', semi_diacritics='hsʃʂʒʐzθɕʑfvθðnmȵŋ', debug=False):
    content = ['Grapheme\tSegments\tCLPA\tStructure\tUnicode\tFrequency\tReflexes\tExamples']
    content += list(get_structure_profile(
        wordlist, language=language, column=column, text=True, semi_diacritics=semi_diacritics,
        debug=debug))
    
    lingpy.util.write_text_file(filename, content, normalize='NFC')
