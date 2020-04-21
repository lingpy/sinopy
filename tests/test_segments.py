from sinopy.segments import *

words = ['piŋ⁵³guo⁵']
for w in words:
    print(' '.join([''.join(x) for x in get_structure(w)]))


