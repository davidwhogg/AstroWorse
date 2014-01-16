# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (C) 2013 AstroWorse
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file LICENSE.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

# WARNING: This code SUX

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import json
import random
import string
import cPickle as pickle

# Project
import nltk
import numpy as np

with open("data/aas_abstracts.json") as f:
    aas_data = json.loads(f.read())

all_tokens = []
for session_num in aas_data.keys():
    aas_data[session_num]
    for pres_num in aas_data[session_num]['presentations'].keys():
        title = filter(lambda x: x in string.printable, aas_data[session_num]['presentations'][pres_num]['title']).lower()
        tokens = nltk.word_tokenize(title)

        all_tokens.append("START")
        all_tokens += tokens
        all_tokens.append("END")

trigrams = nltk.trigrams(all_tokens)
print(len(trigrams), len(np.unique(trigrams)))
str_trigrams = [" ".join(gram) for gram in trigrams]
str_pregrams = np.array([" ".join(gram[:-1]) for gram in trigrams])

unq = np.unique(str_pregrams)

multinomial_family = dict()
for word_pair in unq:
    w, = np.where(str_pregrams == word_pair)
    next_words = []
    for ii in w:
        try:
            next_words.append(trigrams[ii][2])
        except IndexError:
            continue

    next_H = np.zeros(len(next_words))
    for ii,next_word in enumerate(next_words):
        next_H[ii] = next_words.count(next_word)

    xk = np.arange(len(next_H))
    denom = sum(next_H)
    if denom == 0:
        continue

    pk = next_H.astype(float)/denom
    multinomial_family[word_pair] = {"xk" : list(xk.astype(float)),
                                     "pk" : list(pk.astype(float)),
                                     "words" : list(next_words)}

with open("data/trigram.json", "w") as f:
    f.write(json.dumps(multinomial_family))

#rv_discrete(name='trigram_{0}'.format(word_pair), values=(xk,pk))
