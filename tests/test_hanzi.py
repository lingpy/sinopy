"""
Test the hanzi module.
"""
from sinopy.hanzi import (
        compose, decompose, character_from_structure,
        pinyin, chars2baxter, chars2gloss
        )

def test_compose():
    start = '⿰亻⿱立日'
    
    char = compose(start)
    assert char == "偣"


def test_decompose():
    char = decompose("偣")
    assert char == "⿰亻⿱⿱⿱亠丷一日" 


def test_character_from_structure():
    assert character_from_structure('+人我') == '俄'


def test_pinyin():
    assert pinyin('俄') == "é"
    assert pinyin('认得') == "rèn dé"


def test_chars2baxter():

    assert chars2baxter('认得')[0] == "nyinH"
    assert chars2baxter("认得")[1] == "tok"


def test_chars2gloss():
    
    assert chars2gloss('认')[0] == "recognize, know, understand"

