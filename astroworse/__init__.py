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

import views