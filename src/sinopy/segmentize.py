from collections import OrderedDict
try:
    from sinopy.data import _path
except:
    from data import _path
from lingpy import csv2list
# simple segments parser


def segmentize(word, segments, column=False, debug=False):
    

    stack, out = [[[], word, '']], []
    while stack:
        segmented, current, rest = stack.pop(0)
        if current in segments and not rest:
            out += segmented + [current]
        elif len(current) == 1 and current not in segments:
            if rest:
                stack += [[segmented+[current], rest, '']]
            else:
                out += segmented + [current]
        elif current not in segments and current:
            stack += [[segmented, current[:-1], current[-1]+rest]]
        elif not current and rest:
            stack += [[segmented, rest, '']]
        elif current in segments and rest:
            stack += [[segmented+[current], rest, '']]
        if stack and debug:
            print(stack)
            print(stack[-1][0])
            print(stack[-1][1])
            print(stack[-1][2])
            input()
    if column:
        return [segments.get(x, {column: '<'+x+'>'})[column] for x in out]
    return out

if __name__ == '__main__':
    
    segments = ['kh', 'k', 'p', 'ph', 'a', 'e', 'i', 'ei', 'o', 'u']

    out = segmentize('khatphaeit', segments, debug=False)
    print(' '.join(out))

    segments = {
            'kh': {"ipa": 'kʰ'},
            'ph': {"ipa": 'pʰ'},
            'a':  {"ipa": 'a'},
            'e':  {"ipa": 'e'},
            'ei': {"ipa": 'ei'},
            'k':  {"ipa": 'k'},
            'p':  {"ipa": 'p'}}
    out = segmentize('khaetphaeit', segments, debug=False, column='ipa')
    print(' '.join(out))

    segments = {k[0]: {'ipa': k[1], 'structure': k[2]} for k in
            csv2list(_path('chinese.tsv'))}

    for word in [
            'khap55',
            'khuang5',
            'kai',
            'kiAng',
            'thang',
            'pfhang35',
            'pfing44fu24',
            'mao35tse35doŋ51']:
        print(' '.join(segmentize(word, segments, column='ipa')))
        print(' '.join(segmentize(word, segments, column='structure')))
        print(' ')

    
