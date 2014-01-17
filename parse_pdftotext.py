# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (C) 2013 AstroWorse
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file LICENSE.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

# WARNING: This code SUX
# http://astroworse.com/dumbaas/1818733571

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import json
import glob
import re

#pattr = re.compile(r"[0-9]{3}\.[0-9]{2,3}.*$")
pattr = re.compile(r"([0-9]{3}\.[0-9]{2,3})(.*)")

expr1 = r"([A-Za-z\.]+\s(?:(?:[A-Za-z]\.)|(?:[A-Za-z]+))\s[A-Za-z]+\s*[0-9]\,.*)"
bad_pattr1 = re.compile(expr1)
expr2 = r"([A-Za-z\.]+\s(?:(?:[A-Za-z]\.)|(?:[A-Za-z]+))\s[A-Za-z]+\s*[0-9].*)"
bad_pattr2 = re.compile(expr2)

with open("data/aas_abstracts.json") as f:
    data = json.loads(f.read())

for ii,filename in enumerate(glob.glob("data/aas*.txt")):
    with open(filename) as f:
        text = f.read()

    nfailures = 0
    ntotal = 0
    presentations = dict()
    for jj,match in enumerate(pattr.finditer(text)):
        ntotal += 1
        title = match.groups()[1]
        title = title[2:]
        #m = bad_pattr.search(title)
        #if m is not None or len(title) > 500:
        #    if m is not None:
        #        print(m.groups())
        if len(title) > 500:
            nfailures += 1
            continue

        if ',' in title and '.' in title:
            try:
                groups = bad_pattr1.search(title).groups()
            except:
                try:
                    groups = bad_pattr2.search(title).groups()
                except:
                    nfailures += 1
                    continue
            title = title.replace(groups[0],'')

        presentations[jj] = dict(title=title.decode('unicode_escape').encode('ascii','ignore'))

    session = dict(presentations=presentations)
    data[str(ii)] = session

    print("{} failures of {} total".format(nfailures, ntotal))

with open("data/aas_abstracts.json", "w") as f:
    dump = json.dumps(data)
    f.write(dump)


