# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (C) 2013 AstroWorse
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file LICENSE.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import json
import os
import random

# Third-party
import nltk
from flask import request, render_template, redirect, url_for, g
import requests
from scipy.stats import rv_discrete

# Project
from . import app

def load_text():
    r = requests.get("http://deimos.astro.columbia.edu/scratch/trigram.json")
    data = r.json()

    multinomial_family = dict()
    for word_pair in data.keys():
        multinomial_family[word_pair] = dict()
        multinomial_family[word_pair]['dist'] = rv_discrete(name='trigram_{0}'.format(word_pair), values=(data[word_pair]['xk'],data[word_pair]['pk']))
        multinomial_family[word_pair]['words'] = data[word_pair]['words']

    g.model = multinomial_family

@app.route('/')
def index():
    try:
        model = g.model
    except:
        load_text()
        model = g.model

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

    return "<html><h3>{}</h3></html>".format(better_sentence)

