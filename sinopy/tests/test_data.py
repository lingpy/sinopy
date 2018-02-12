from __future__ import unicode_literals, division

def test_unihan():
    from sinopy.data import UNIHAN
    assert UNIHAN['分']['mandarin'] == 'fēn'

def test_character_from_structure():
    from sinopy.sinopy import character_from_structure
    assert character_from_structure('+手羅') == '攞'
