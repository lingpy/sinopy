from __future__ import unicode_literals, division

def test_unihan():
    from sinopy.data import UNIHAN
    assert UNIHAN['分']['mandarin'] == 'fēn'


