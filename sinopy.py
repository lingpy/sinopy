# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-02-06 14:04
# modified : 2015-02-07 21:58
"""
Python script for NLP operatins in Chinese dialectology.
"""

__author__="Johann-Mattis List"
__date__="2015-02-07"

import lingpyd as lingpy
import json
from . import chinese_data as _cd

# we try to add as many distinct operations as possible here, including
# automatic segmentizer for chinese syllables and other things


def parse_baxter(reading):
    """
    Parse a Baxter string and render it with all its contents, namely
    initial, medial, final, and tone.
    """

    initial = ''
    medial = ''
    final = ''
    tone = ''
    
    # determine environments
    inienv = True
    medienv = False
    finenv = False
    tonenv = False

    inichars = "pbmrtdnkgnsyhzl'x"
    

    chars = list(reading)
    for char in chars:
        
        # switch environments
        if char in 'jw' and not finenv:
            inienv,medienv,finenv,tonenv = False,True,False,False
        elif char not in inichars or finenv:
            if char in 'XH':
                inienv,medienv,finenv,tonenv = False,False,False,True
            else:
                inienv,medienv,finenv,tonenv = False,False,True,False
        
        # fill in slots
        if inienv:
            initial += char
            
        if medienv:
            medial += char

        if finenv:
            final += char

        if tonenv:
            tone += char

    # post-parse tone
    if not tone and final[-1] in 'ptk':
        tone = 'R'
    elif not tone:
        tone = 'P'

    # post-parse medial
    if 'j' not in medial and 'y' in initial:
        medial += 'j'

    # post-parse labial
    if final[0] in 'u' and 'w' not in medial:
        medial = 'w' + medial

    return initial,medial,final,tone

def chars2baxter(chars):
    """
    Convert a sequence of Characters to their MCH values.
    """

    out = []
    chars = gbk2big5(chars)

    for char in chars:
        tmp = []
        if char in _cd.TLS:
            for entry in _cd.TLS[char]:
                baxter = _cd.TLS[char][entry]['BAXTER']
                if baxter != '?':
                    tmp += [baxter]
        out += [','.join(tmp)]
    return out


def sixtuple2baxter(chars, debug=False):
    """ 
    Convert the classicial six-tuple representation of MCH readings into IPA
    (or Baxter's ASCII system). 
    This function is more or less implemented in MiddleChinese.
    """

    if len(chars) != 6:
        raise ValueError('chars should be a sixtuple')
    
    # convert chars to long chars
    chars = gbk2big5(chars)

    # assign basic values
    she,hu,deng,diao,yun,sheng = list(chars) 
    
    # try converting the values to mch representations
    initial = _cd.GY['sheng'].get(sheng)
    final = _cd.GY['yun'].get(yun)
    tone = _cd.GY['diao'].get(diao)
    medial = _cd.GY['hu'].get(hu)
    division = _cd.GY['deng'].get(deng)
    
    # debug is for cross-checking
    if debug:
        return [initial,medial,division,final,tone]

    # treat the final if division is 3 and they start with 'j', note that so
    # far, we don't handle chongnius
    final = final[1:] if final[0] == 'j' and division in '4' \
            else final
    final = final[1:] if final[0] == 'j' and division in '3' \
            else final

    # reduce finals starting with 'w'
    final = final[1:] if final[0] == 'w' else final
    
    # resolve the medial (the hu) by checking for labial initial
    medial = '' if (initial[0] in 'pbm' and '*' not in final) \
            or final[0] in 'u' \
            or 'o' in final and not '*' in final and not '?' in final \
            else medial
    
    # correct for initials with sandeng-i
    initial = initial[:-1] if initial.endswith('j') else initial

    # get the medial corrected by deng
    medial = "j" + medial if division == '3' \
            and 'i' not in final \
            and 'y' not in initial \
            else medial

    # deprive the rime from its leading "j" if we have a medial
    final = final[1:] if final[0] in 'j' and 'j' in medial else final
    final = final[1:] if final[0] in 'w' and 'w' in medial else final
    final = final[1:] if final[0] == '*' or final[0] == '?' else final
    final = 'i' + final[1:] if final[0] == '!' \
            and division == '4' \
            and 'i' not in final \
            and (initial[0] in "pbmkgx'" or initial.startswith('ng')) \
            else final

    # chongniu medial-re-order
    medial = 'j' + medial if division == '4' \
            and '!' in final \
            and 'j' not in medial \
            and (initial[0] in "pbmkgx'" or initial.startswith('ng')) \
            else medial

    final = final[1:] if final[0] == '!' else final
    
    # put everything together
    return [initial,medial,final,tone]
  
def normalize_pinyin(pinyin):
    """
    Normalize pinyin representation by replacing numbers with diaecritics.
    """
    
    pass

def analyze_sequence(ipa):
    """
    Convert a normal ipa string into a prostring for Chinese dialects.
    """
    # we need some very good strategy here, which should be lightwayt and easy
    # to re-implement in other languages (e.g. JS)

    # get sound-class rep of stirng first
    seqs = re.split('([₁₂₃₄₅₆₀¹²³⁴⁵⁶⁰])+', ipa)
    out = ''
    for i in range(len(seqs)):
        seqs = ipa2tokens(tokens2class(ipa, merge_vowels=False, expand_nasals=True),'asjp')
    
        D = {}

        pass

def fanqie2mch(fanqie, debug=False):
    """
    Convert a Fǎnqiè reading to it's MCH counterpart.
    
    Important: we need to identify the medials in the xia-syllable. We also
    need to make additional background-checks, since in the current form, the
    approach is not error-prone and does not what it is supposed to do! 
    """
    
    # check for gbk
    fanqie = gbk2big5(fanqie)
    
    # get normal vals
    shangxia = chars2baxter(fanqie)
   
    # check for good fixed solutions in our dictionary
    if fanqie[0] in _cd.GY['sheng']:
        shang = _cd.GY['sheng'][fanqie[0]]+'a'
    else:
        shang = shangxia[0]

    xia = shangxia[1]

    # check for bad vals
    if ' ' in shang:
        shang = shang[:shang.index(' ')]
    if ' ' in xia:
        xia = xia[:xia.index(' ')]

    if ',' in shang or ',' in xia or not shang or not xia:
        raise ValueError('fanqie {0} {1} is ambiguous'.format(shang,xia))
    
    # parse chars
    shangp = parse_baxter(shang)
    xiap = parse_baxter(xia)
    
    if debug:
        return '.'.join(shangp),'.'.join(xiap),shang,xia
    
    i = shangp[0]
    m = xiap[1]
    f = xiap[2]
    t = xiap[3].replace('P','').replace('R','') # ugly, change later XXX
    
    # clean medial-relations
    if ('y' in i or 'i' in f) and 'j' in m:
        m = m.replace('j','')
    if 'u' in f and 'w' in m:
        m = m.replace('w','')
        
    return ''.join([i,m,f,t]) 

def baxter2ipa(mch):
    """
    Very simple aber convient-enough conversion from baxter MCH to IPA MCH.
    this is also more or less already implemented in MiddleChinese
    """

    out = mch
    if out[-1] in 'ptk':
        out += 'R'
    elif out[-1] not in 'XHP':
        out += 'P'
        
    for s,t in _cd.GY['ipa']: #XXX replace possibly by another funciton
        out = out.replace(s,t)
    return out

def gbk2big5(chars):
    """
    Convert from gbk format to big5 representation of chars.
    """
    
    out = ''
    for char in chars:
        if char in _cd.GBK:
            out += _cd.BIG5[_cd.GBK.index(char)]
        else:
            out += char
    return out

def big52gbk(chars):
    """
    Convert from long chars to short chars.
    """

    out = ''
    for char in chars:
        if char in _cd.BIG5:
            out += _cd.GBK[_cd.BIG5.index(char)]
        else:
            out += char


def clean_chinese_ipa(seq):

    tones = list(zip('0123456','¹²³⁴⁵⁶'))

    st = [('tsh', "ʦʰ"),
          ('ts', 'ʦ'),
          ("th","tʰ"),
          ("kh","kʰ"),
          ("ph","pʰ"),
          ("pfh","p͡fʰ"),
          ("pf","p͡f"),
          ('dz', "ʣ")
          ]
    st = sorted(st, key=lambda x: len(x[0]), reverse=True)

    for s,t in tones:
        seq = seq.replace(s,t)
    for s,t in st:
        seq = seq.replace(s,t)

    if ' ' in seq:
        seq = seq.replace(' ','')

    return seq


if __name__ == '__main__':

    td = sorted(set([(a,b) for a,b in lingpy.csv2list('test_data')]))
    
    good = 0
    failed_rime = 0
    diff = 0
    nomch = 0

    for char,chars in td:
        try:
            fanqie = chars[-1] + chars[-2]
            baxter = '//'.join(chars2baxter(char))
            mch = fanqie2mch(fanqie)
        
            if mch not in baxter:
                print(char, baxter,mch, fanqie2mch(fanqie, debug=True), fanqie)
                diff += 1
        except ValueError:
            print (chars, chars2baxter(fanqie[0]),
                    chars2baxter(fanqie[1]),fanqie)

    print(diff)
    #for char,chars in td:
    #    
    #    
    #    baxter = '//'.join(chars2baxter(char))

    #    try:
    #        mchA = sixtuple2baxter(chars)
    #        mch = ''.join(mchA).replace('P','').replace('R','')

    #        if mch in baxter:
    #            good += 1
    #        elif '//'.join(baxter):
    #            if 'ji' in baxter or 'ji' in mch: 
    #                print(char,'\t','{0:20}'.format(baxter),'\t','{0:10}'.format(mch),'\t',
    #                        '\t'.join(mchA),'\t=>\t','\t'.join(
    #                    sixtuple2baxter(chars,debug=True)))
    #            diff += 1
    #        else:
    #            nomch += 1

    #    except:
    #        failed_rime += 1

    #print(good,failed_rime,diff,nomch, len(td))

