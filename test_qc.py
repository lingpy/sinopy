from MiddleChinese import *
import json
from lingpyd import *
import chinese

char2mch = json.loads(open('data/tls.json').read())

short2long = lambda x: ''.join([chinese.gbk2big5(y) for y in x])
long2short = lambda x: ''.join([chinese.big52gbk(y) for y in x])

tests = sorted(set([(a,short2long(b)) for a,b in csv2list('test_data')]))

# now we convert and check how good it is
def get_mchr(char):

    if char in char2mch:
        idxs = char2mch[char]
        readings = [char2mch[char][idx]['BAXTER'] for idx in idxs]
    else:
        if chinese.gbk2big5(char) in char2mch:
            return get_mchr(chinese.gbk2big5(char))
        else:
            readings = []
    return readings

count = 0
for char,chars in tests:


    try:
        w = Wang(chars)
        mch = w.wang2baxter().replace('P','').replace('R','')
    
        readings = get_mchr(char)

        if mch not in readings:
            fanqies = get_mchr(chars[0])[0]+' '+get_mchr(chars[-1])[0]+' '+get_mchr(chars[-2])[0]


            print(char,'\t',mch, '\t',','.join(readings),
                    '\t',chars[-2],chars[-1], fanqies)
        else:
            print(mch, ','.join(readings))
            count += 1
    except:
        print('[!]',char,chars)

print(count, len(tests))
#tests = []
#wl = Wordlist('yinku.qlc')
#for k in wl:
#    
#    zgyy = wl[k,'zgyy']
#    char = wl[k,'gloss']
#
#    if zgyy not in tests:
#        tests += [(char,zgyy)]



