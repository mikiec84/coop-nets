import collections
import re
from jieba import tokenize as jieba_tokenize
from hanziconv import HanziConv as hanzi

WORD_RE_STR = r"""
(?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
|
(?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
|
(?:[\w_]+)                     # Words without apostrophes or dashes.
|
(?:\.(?:\s*\.){1,})            # Ellipsis dots.
|
(?:\*{1,})                     # Asterisk runs.
|
(?:\S)                         # Everything else that isn't whitespace.
"""

WORD_RE = re.compile(r"(%s)" % WORD_RE_STR, re.VERBOSE | re.I | re.UNICODE)


def basic_unigram_tokenizer(s, lower=True):
    words = WORD_RE.findall(s)
    if lower:
        words = [w.lower() for w in words]
    return words


def heuristic_ending_tokenizer(s, lower=True):
    words = basic_unigram_tokenizer(s, lower=lower)
    return [seg for w in words for seg in heuristic_segmenter(w)]


ENDINGS = ['er', 'est', 'ish']


def heuristic_segmenter(word):
    for ending in ENDINGS:
        if word.endswith(ending):
            return [word[:-len(ending)], '+' + ending]
    return [word]


def whitespace_tokenizer(s, lower=True):
    if lower:
        s = s.lower()
    return s.split()


def chinese_tokenizer(s, lower=True):
    s = unicode(s)
    if lower:
        s = hanzi.toSimplified(s)
    return [t[0] for t in jieba_tokenize(s)]


TOKENIZER_MAP = {
    'en': heuristic_ending_tokenizer,
    'zh': chinese_tokenizer,
}


def multilingual_tokenizer(s, lower=True):
    assert isinstance(s, basestring) and u':' in s, repr(s)
    lang, utt = s.split(u':', 1)
    return TOKENIZER_MAP[lang](utt, lower=lower)


NOENDING_TOKENIZER_MAP = {
    'en': basic_unigram_tokenizer,
    'zh': chinese_tokenizer,
}


def multilingual_noending_tokenizer(s, lower=True):
    assert isinstance(s, basestring) and u':' in s, repr(s)
    lang, utt = s.split(u':', 1)
    return NOENDING_TOKENIZER_MAP[lang](utt, lower=lower)


TOKENIZERS = {
    'unigram': basic_unigram_tokenizer,
    'ending': heuristic_ending_tokenizer,
    'whitespace': whitespace_tokenizer,
    'chinese': chinese_tokenizer,
    'multilingual': multilingual_tokenizer,
    'multilingual_noending': multilingual_noending_tokenizer,
}
