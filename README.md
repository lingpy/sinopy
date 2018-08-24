# SinoPy: Python Library for Handling Chinese and Sino-Tibetan Language Data

This is intended as a plugin for LingPy, or an addon, however, you define "plugin". The library gives utility functions that prove useful to handle Chinese data in a very broad context, raning from Chinese character readings up to proposed readings in Middle Chinese and older stages of the language.

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


