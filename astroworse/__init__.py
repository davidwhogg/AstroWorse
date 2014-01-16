# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (C) 2013 AstroWorse
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file LICENSE.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

from flask import Flask

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!lskjflkjsf 33has$$'

def build_model():
    from scipy.stats import rv_discrete
    import json
    import os

    with open(os.path.join(os.environ['ASTROWORSE'], "data/trigram.json")) as f:
        data = json.loads(f.read())

    model = dict()
    for word_pair in data.keys():
        model[word_pair] = dict()
        model[word_pair]['dist'] = rv_discrete(name='trigram_{0}'.format(word_pair),
            values=(data[word_pair]['xk'],data[word_pair]['pk']))
        model[word_pair]['words'] = data[word_pair]['words']

    print("model built")

    return model

trigram_model = build_model()

import views