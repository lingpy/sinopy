from sinopy.hanzi import (
        compose, decompose, character_from_structure,
        pinyin, chars2baxter, chars2gloss
        )

start = '⿰亻⿱立日'

char = compose(start)
print(char, char == "偣")

comps = decompose(char)
print(comps)

char2 = compose(comps)
print(char, char2) 

print(character_from_structure('+人我') == '俄')

print(pinyin('俄'))
# gbk
print(pinyin('认得'))

print(chars2baxter('认得'))
print(chars2gloss('认得'))

