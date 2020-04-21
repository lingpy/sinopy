from sinopy.seaquence import parse_chinese_morphemes, get_structure

for seq in [
        'waŋ⁵⁵',
        'fəŋ³¹',
        'piao⁴',
        'put⁵',
        'tsʰ a i j ⁵¹',
        'kiaoŋ⁰'
        ]:
    print(seq)
    print('\t'.join([x for x in parse_chinese_morphemes(seq) if x != '-']))
    print('\t'.join(list(get_structure(seq))[0]))
    print('---')
