from sinopy.segments import *
from pyburmish.dataset import Dataset

words = ['piŋ⁵³guo⁵']
for w in words:
    print(' '.join([''.join(x) for x in get_structure(w)]))

ds = Dataset('Mann1998')
prf = get_structure_profile(ds.words, column='tokens')
write_structure_profile(ds.words, column='tokens')
