# SinoPy: Python Library for quantitative tasks in Chinese historical linguistics

[![DOI](https://zenodo.org/badge/30593438.svg)](https://zenodo.org/badge/latestdoi/30593438)
![PyPI](https://img.shields.io/pypi/v/sinopy.svg)

SinoPy is an attempt to provide useful functionality for users working with Chinese dialects and Sino-Tibetan language data and struggling with tasks like converting characters to Pinyin, analysing characters, or analysing readings in Chinese dialects and other SEA languages. 

If you use the library in your research, please quote it as:

> List, Johann-Mattis (2018): SinoPy: Python Library for quantitative tasks in Chinese historical linguistics. Version 0.3.0. Jena: Max Planck Institute for the Science of Human History. DOI: https://zenodo.org/badge/latestdoi/30593438

This is intended as a plugin for LingPy, or an addon. The library gives utility functions that prove useful to handle Chinese data in a very broad context, ranging from Chinese character readings up to proposed readings in Middle Chinese and older stages of the language.

## Quick Usage Examples

Convert Baxter's (1992) Middle Chinese transcription system to plain IPA (with tone marks).

```python
>>> from sinopy import baxter2ipa
>>> baxter2ipa('bjang')
'bjaŋ¹'
>>> baxter2ipa('bjang', segmented=True)
['b', 'j', 'a', 'ŋ', '¹']
```

Convert Chinese characters to Pīnyīn

```python
>>> from sinopy import pinyin
>>> pinyin('我', variant='cantonese')
'ngo5'
>>> pinyin('我', variant='mandarin')
'wǒ'
```

Try to find character by combining two characters:

```python
>>> from sinopy import character_from_structure
>>> character_from_structure('+人我')
'俄'
```

## More examples

At the moment, you may have difficulties finding a common idea behind SinoPy,
as the collection of scripts is very diverse. The general topic, however, are
basic operations one frequently encounters when working with Chinese and SEA
linguistic data.

But let's just look at a couple of examples:

```python
>>> from sinopy import *
>>> char = "我"
>>> pinyin(char, variant="mandarin")
wǒ
```

So obviously, we can convert characters to Pīnyīn.

```python
>>> is_chinese(char)
True
>>> is_chinese('b')
False
```

So the library also checks if a character belongs to Chinese Unicode range.

But we have also a range of functions for handling Middle Chinese and related problems. For example the following:

```python
>>> parse_baxter('ngaH')
('ng', '', 'a', 'H')
```

So this function will read in a Middle Chinese string (as encoded in the system of Baxter 1992) and return its main constituents (initial, medial, final, and tone).

But we can also directly convert a character to its Middle Chinese reading:

```python
>>> chars2baxter(char)
['ngaX']
```

Or we can retrieve a basic gloss.

```python
>>> chars2gloss(char)
['our, us, i, me, my, we']
```

A rather complex function is the `sixtuple2baxter` function, which reads in the classical six-character descriptions of the Middle Chinese reading of a given character and yields the Middle Chinese value following Baxter's system. You find a lot of sixtuple readings in the DOC database (published with the [Tower of Babel project](http://starling.rinet.ru/cgi-bin/response.cgi?root=config&morpho=0&basename=\data\china\doc&first=1)).

```python
>>> sixtuple2baxter('蟹開一上海泥')                            
['n', '', 'oj', 'X']
>>> chars2baxter('乃')                 
['nojX']
```

You can also directly try to retrieve the MC reading from passing two fǎnqiè characters, for example:

```python
>>> fanqie2mch('海泥')
'xej'
>>> fanqie2mch('泥海')
'nojX'
```

And if you don't like Baxter's MCH transcriptions, you can simply turn it to IPA:

```python
>>> baxter2ipa('nojX')
noj²
>>> baxter2ipa('tsyang')
'ʨaŋ¹'
```

As a final important function, consider the parser for morphemes:

```python
>>> parse_chinese_morphemes('ʨaŋ¹')
['ʨ', '-', 'a', 'ŋ', '¹']
```

The quintuple that he method returns splits the sequence into its five main constituents, initial, medial, nucleus, coda, and tone. 

