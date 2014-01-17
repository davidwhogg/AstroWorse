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
import glob
import re

#pattr = re.compile(r"[0-9]{3}\.[0-9]{2,3}.*$")
pattr = re.compile(r"([0-9]{3}\.[0-9]{2,3})(.*)")

with open("data/aas_abstracts.json") as f:
    data = json.loads(f.read())

for ii,filename in enumerate(glob.glob("data/aas*.txt")):
    with open(filename) as f:
        text = f.read()

    if data.has_key(str(ii)):
        print("skipping {}".format(filename))
        continue

    nfailures = 0
    ntotal = 0
    presentations = dict()
    for jj,match in enumerate(pattr.finditer(text)):
        ntotal += 1
        title = match.groups()[1]
        title = title[2:]
        if len(title) > 500:
            nfailures += 1
            continue

        presentations[jj] = dict(title=title.decode('unicode_escape').encode('ascii','ignore'))

    session = dict(presentations=presentations)
    data[str(ii)] = session

    print("{} failures of {} total".format(nfailures, ntotal))

with open("data/aas_abstracts.json", "w") as f:
    dump = json.dumps(data)
    f.write(dump)


