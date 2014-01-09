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
from flask import request, render_template, redirect, url_for, g, jsonify, session
import nltk
import requests
from scipy.stats import rv_discrete

# Project
from . import app

def load_text():
    r = requests.get("http://deimos.astro.columbia.edu/scratch/trigram.json")
    data = r.json()
    session['data'] = data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/title')
def get_title():
    try:
        data = session['data']
    except:
        print("loading text")
        load_text()
        data = session['data']

    model = dict()
    for word_pair in data.keys():
        model[word_pair] = dict()
        model[word_pair]['dist'] = rv_discrete(name='trigram_{0}'.format(word_pair), values=(data[word_pair]['xk'],data[word_pair]['pk']))
        model[word_pair]['words'] = data[word_pair]['words']

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

    return jsonify(title=better_sentence)
