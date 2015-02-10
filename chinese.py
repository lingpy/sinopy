# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-01-30 08:17
# modified : 2015-01-30 08:17
"""
LingPy plugin providing basic operations to deal with Chinese characters and \
        ancient Chinese character readings.
"""

__author__="Johann-Mattis List"
__date__="2015-01-30"

import lingpyd as lingpy
import chinese_data as cd

def gbk2big5(char):
    """
    Convert between short and long chars in Chinese.
    """

    if char in cd.BIG5:
        return char
    elif char in cd.GBK:
        return cd.BIG5[cd.GBK.index(char)]
    else:
        return char

def big52gbk(char):
    """
    Convert between short and long chars in Chinese.
    """

    if char in cd.GBK:
        return char
    elif char in cd.BIG5:
        return cd.GBK[cd.BIG5.index(char)]
    else:
        return char

def char2mch(char):
    "Function returns data on Chinese characers."

    nchar = gbk2big5(char)

    if nchar in cd.MCH:

        return cd.MCH[nchar]
    else:
        return ["?","?"]

def char2mch_baxter(char):

    return char2mch(char)[0]

def char2mch_ipa(char):
    
    return char2mch(char)[1]

def chars2mch(charstring, mode='ipa'):
    
    out = []
    for char in charstring.strip():
        if mode == 'ipa':
            out += [char2mch_ipa(char)]
        else:
            out += [char2mch_baxter(char)]
    if mode == 'ipa':
        return ' '.join(
            lingpy.ipa2tokens(lingpy.rc('morpheme_separator').join(out))
            )
    else:
        return '-'.join(out)
    

if __name__ == '__main__':

    chars = ["红","黄","黑","多","少","大","小","粗","细","长","短","宽","窄","高","矮","高","低","歪","弯","陡","咸","淡","厚","薄","稠","稀","密","稀","亮","黑","热","冷","干","湿","干","脏","快","快","慢","早","晚","对","错","漂","丑"]

    for char in chars:
        print(char, gbk2big5(char), char2mch_baxter(char), char2mch_ipa(char))
