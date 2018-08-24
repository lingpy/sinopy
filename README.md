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


