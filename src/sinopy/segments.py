import lingpy
from lingpy.sequence.sound_classes import tokens2morphemes, codepoint, tokens2class
from sinopy.sinopy import parse_chinese_morphemes
from collections import defaultdict
from lingpy import log

def strip_chars(chars, string):
    return ''.join([c for c in string if c not in chars])

def get_structure(word, sep='+', zipped=False, semi_diacritics='hsʃʂʒʐzθɕʑfvθðnmȵ'):
    if not isinstance(word, (list, tuple)):
        word = lingpy.ipa2tokens(word, expand_nasals=True, merge_vowels=False,
                semi_diacritics=semi_diacritics)

    # check for unknown chars
    try: 
        tokens2class(word, 'cv', cldf=True)
    except ValueError:
        print('problem with {0}'.format(''.join(word)))
        return []

    # get the morphemes
    if sep in word:
        words = tokens2morphemes(word, cldf=True)
        morphemes = []
        for w in words:
            morphemes += tokens2morphemes(w, sep=sep)
    else:
        morphemes = tokens2morphemes(word, cldf=True)
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

def get_structure_profile(wordlist, column='ipa', text=False,
        semi_diacritics='hsʃʂʒʐzθɕʑfvθð', debug=False, language=None):
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
