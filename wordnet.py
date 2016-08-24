# -*- coding: utf-8 -*-
"""
=============================================================================================
1.wordnet
    To provide the functionality of front-end in Python of Japanese WordNet.
---------------------------------------------------------------------------------------------
    *** Reference(many thanks) ***
    http://subtech.g.hatena.ne.jp/y_yanbe/20090314/p2
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
"""
import sys
import sqlite3
from collections import namedtuple

# ===========================================================================================
# Connect to sqllite3(Japanese WordNet)
# ===========================================================================================
conn = sqlite3.connect("wnjpn-0.9.db")
Word = namedtuple('Word', 'wordid lang lemma pron pos')

# ===========================================================================================
# getWords
# ===========================================================================================
def getWords(lemma):
    words = []
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    row = cur.fetchone()
    while row:
        words.append(Word(*row))
        row = cur.fetchone()
    return words

# ===========================================================================================
# getWord
# ===========================================================================================
def getWord(wordid):
    cur = conn.execute("select * from word where wordid=?", (wordid,))
    return Word(*cur.fetchone())
 
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

# ===========================================================================================
# getSenses
# ===========================================================================================
def getSenses(word):
    senses = []
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    row = cur.fetchone()
    while row:
        senses.append(Sense(*row))
        row = cur.fetchone()
    return senses

# ===========================================================================================
# getSense
# ===========================================================================================
def getSense(synset, lang='jpn'):
    cur = conn.execute("select * from sense where synset=? and lang=?", (synset,lang))
    row = cur.fetchone()
    if row:
        return Sense(*row)
    else:
        return None

Synset = namedtuple('Synset', 'synset pos name src')

# ===========================================================================================
# getSynset
# ===========================================================================================
def getSynset(synset):
    cur = conn.execute("select * from synset where synset=?", (synset,))
    row = cur.fetchone()
    if row:
        return Synset(*row)
    else:
        return None

SynLink = namedtuple('SynLink', 'synset1 synset2 link src')

# ===========================================================================================
# getSynLinks
# ===========================================================================================
def getSynLinks(sense, link):
    synLinks = []
    cur = conn.execute("select * from synlink where synset1=? and link=?", (sense.synset, link))
    row = cur.fetchone()
    while row:
        synLinks.append(SynLink(*row))
        row = cur.fetchone()
    return synLinks

# ===========================================================================================
# getSynLinksRecursive
# ===========================================================================================
def getSynLinksRecursive(senses, link, lang='jpn', _depth=0):
    for sense in senses:
        synLinks = getSynLinks(sense, link)
        if synLinks:
            print '  '*_depth + getWord(sense.wordid).lemma, getSynset(sense.synset).name
        _senses = []
        for synLink in synLinks:
            sense = getSense(synLink.synset2, lang)
            if sense:
                _senses.append(sense)
        getSynLinksRecursive(_senses, link, lang, _depth+1)


# ===========================================================================================
# Reads the data file
# Data file is a newline character to separate the code that depends on the OS space and,
# given x, y, label {0,1}
# ===========================================================================================
# -------------------------------------------------------------------------------------------
# Initial processing
# -------------------------------------------------------------------------------------------
words = getWords("負けず嫌い".decode('utf-8'))
if words:
    sense = getSenses(words[0])
    link = "hype"
    result = getSynLinksRecursive(sense, link, "jpn")
    print "result:", result
else:
    print >> sys.stderr, "(nothing found)"
    
"""usage: wn.py word link [lang]
    word
      word to investigate
    
    link
      syns - Synonyms
      hype - Hypernyms
      inst - Instances
      hypo - Hyponym
      hasi - Has Instance
      mero - Meronyms
      mmem - Meronyms --- Member
      msub - Meronyms --- Substance
      mprt - Meronyms --- Part
      holo - Holonyms
      hmem - Holonyms --- Member
      hsub - Holonyms --- Substance
      hprt - Holonyms -- Part
      attr - Attributes
      sim - Similar to
      entag - Entails
      causg - Causes
      dmncg - Domain --- Category
      dmnug - Domain --- Usage
      dmnrg - Domain --- Region
      dmtcg - In Domain --- Category
      dmtug - In Domain --- Usage
      dmtrg - In Domain --- Region
      antsg - Antonyms
    
    lang (default: jpn) 
      jpn - Japanese
      eng - English
"""
