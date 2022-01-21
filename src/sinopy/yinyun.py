import lingpy
import json
from sinopy import data as sdata
from sinopy.util import is_chinese
import re
from sinopy.hanzi import gbk2big5

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

    return initial, medial, final, tone


def sixtuple2baxter(chars, debug=False, rhymebook=None):
    """ 
    Convert the classicial six-tuple representation of MCH readings into IPA
    (or Baxter's ASCII system). 
    This function is more or less implemented in MiddleChinese.
    """
    if not rhymebook:
        rhymebook = sdata.GY

    if len(chars) != 6:
        raise ValueError('chars should be a sixtuple')
    
    # convert chars to long chars
    chars = gbk2big5(chars)

    # assign basic values
    she,hu,deng,diao,yun,sheng = list(chars) 
    
    # try converting the values to mch representations
    initial = rhymebook['sheng'].get(sheng, '?')
    final = rhymebook['yun'].get(yun, '?')
    tone = rhymebook['diao'].get(diao, '?')
    medial = rhymebook['hu'].get(hu, '?')
    division = rhymebook['deng'].get(deng, '?')
        
    # debug is for cross-checking
    if debug:
        return [(sheng, initial), (hu, medial), (deng, division),(yun, final),
                (diao, tone)]

    # check and raise error if things are not handled
    if "?" in [initial, final, tone, medial, division]:
        raise ValueError("Unrecognized elements in {0}.".format(
            ' '.join([initial, final, tone, medial, division])))

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


def baxter2ipa(mch, segmented=False):
    """
    Very simple aber convient-enough conversion from baxter MCH to IPA MCH.
    this is also more or less already implemented in MiddleChinese
    """

    out = mch
    if out[-1] in 'ptk':
        out += 'R'
    elif out[-1] not in 'XHP':
        out += 'P'
        
    for s, t in sdata.GY['ipa']: 
        out = out.replace(s, t)
    if segmented:
        return parse_chinese_morphemes(out) 
    return out
