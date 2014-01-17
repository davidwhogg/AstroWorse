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

# Third-party
from flask import request, render_template, redirect, url_for, g, jsonify, session
import nltk
import numpy as np
from scipy.stats import rv_discrete

# Project
from . import app, trigram_model

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dumbaas/', defaults={'seed':None})
@app.route('/dumbaas/<int:seed>')
def dumbaas(seed=None):
    if seed is None:
        seed = np.random.randint(int(1e10))
    return render_template("dumb-aas.html", seed=seed)

@app.route('/dumbaas/title')
@app.route('/dumbaas/title/<int:seed>')
def get_title(seed=None):
    if seed is not None:
        np.random.seed(seed)

    # sample the first word pair
    start_pairs = []
    for key in trigram_model.keys():
        if key.split()[0] == "START":
            start_pairs.append(key)

    start_pair = np.random.choice(start_pairs)
    word = trigram_model[start_pair]['words'][trigram_model[start_pair]['dist'].rvs()]

    current_bigram = (start_pair.split()[1], word)
    words = list(start_pair.split())
    while True:
        pair = " ".join(current_bigram)
        word = trigram_model[pair]['words'][trigram_model[pair]['dist'].rvs()]
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

    return jsonify(title=better_sentence.strip().capitalize())

