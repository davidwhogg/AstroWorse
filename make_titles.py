# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (C) 2013 AstroWorse
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file LICENSE.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

""" Generates the specified number of talk titles and caches to a JSON file """

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
from scipy.stats import rv_discrete

Ntitles = 10

with open("data/trigram.json") as f:
    data = json.loads(f.read())

print("trigram data loaded")

model = dict()
for word_pair in data.keys():
    model[word_pair] = dict()
    model[word_pair]['dist'] = rv_discrete(name='trigram_{0}'.format(word_pair), values=(data[word_pair]['xk'],data[word_pair]['pk']))
    model[word_pair]['words'] = data[word_pair]['words']

print("model built")

for ii in range(Ntitles):
    print(ii)
    # sample the first word pair
    start_pairs = []
    for key in model.keys():
        if key.split()[0] == "START":
            start_pairs.append(key)

    start_pair = random.choice(start_pairs)
    word = model[start_pair]['words'][model[start_pair]['dist'].rvs()]

    current_bigram = (start_pair.split()[1], word)
    words = list(start_pair.split())
    while True:
        pair = " ".join(current_bigram)
        word = model[pair]['words'][model[pair]['dist'].rvs()]
        current_bigram = (current_bigram[1], word)
        words.append(word)
        if word == "END":
            break

    sentence = " ".join(words[1:-1])
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    better_sentence = ""
    for ii,token in enumerate(tokens):
        if tagged[ii][1] in '.,:\'\"':
            better_sentence += token
        else:
            better_sentence += " {}".format(token)

    print(better_sentence)