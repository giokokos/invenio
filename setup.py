## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Invenio
-----

Invenio is a digital library framework. And before you ask:
It's GNU/GPLv2 licensed!

Invenio is Fun
``````````````

.. code:: python

    from invenio.base import create_app
    app = create_app()

    if __name__ == "__main__":
        app.run()

And Easy to Setup
`````````````````

.. code:: bash

    $ pip install invenio
    $ python hello.py
     * Running on http://localhost:5000/

Links
`````

* `website <http://invenio-software.org/>`_
* `documentation <TODO>`_
* `development version <http://invenio-software.org/repo/invenio>`_

"""
from __future__ import print_function
from setuptools import Command, setup, find_packages
from distutils.extension import Extension

import os

def requirements():
    req = []
    dep = []
    for filename in ['requirements.txt', 'requirements-extras.txt',
                     'requirements-flask.txt', 'requirements-flask-ext.txt']:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                if '://' in line:
                    dep.append(str(line[:-1]))
                else:
                    req.append(str(line))
    return req, dep

packages = find_packages(exclude=['docs'])
packages.append('invenio_docs')

install_requires, dependency_links = requirements()

setup(
    name='Invenio',
    version='1.9999-dev',
    url='http://invenio-sofrware.org/repo/invenio',
    license='GPLv2',
    author='CERN',
    author_email='info@invenio-software.org',
    description='Digital library software',
    long_description=__doc__,
    packages=packages,
    package_dir={'invenio_docs': 'docs'},
    ext_modules=[
        Extension("invenio.intbitset",
                  ["invenio/intbitset.c", "invenio/intbitset_impl.c"],
                  extra_compile_args=['-O3'])
                  ## For debug -> '-ftree-vectorizer-verbose=2'
    ],
    #namespace_packages=['invenio'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'inveniomanage = invenio.base.manage:main',
            'plotextractor = invenio.utils.scripts.plotextractor:main',
            ## Legacy
            'alertengine = invenio.legacy.webalert.scripts.alertengine:main',
            'batchuploader = invenio.legacy.bibupload.scripts.batchuploader',
            'bibcircd = invenio.legacy.bibcirculation.scripts.bibcircd:main',
            'bibauthorid = invenio.legacy.bibauthorid.scripts.bibauthorid:main',
            'bibclassify = invenio.modules.classifier.scripts.classifier:main',
            'bibconvert = invenio.legacy.bibconvert.scripts.bibconvert:main',
            'bibdocfile = invenio.legacy.bibdocfile.scripts.bibdocfile:main',
            'bibedit = invenio.legacy.bibedit.scripts.bibedit:main',
            'bibencode = invenio.modules.encoder.scripts.encoder:main',
            'bibindex = invenio.legacy.bibindex.scripts.bibindex:main',
            'bibmatch = invenio.legacy.bibmatch.scripts.bibmatch:main',
            'bibrank = invenio.legacy.bibrank.scripts.bibrank:main',
            'bibrankgkb = invenio.legacy.bibrank.scripts.bibrankgkb:main',
            'bibreformat = invenio.legacy.bibformat.scripts.bibreformat:main',
            'bibsort = invenio.legacy.bibsort.scripts.bibsort:main',
            'bibsched = invenio.legacy.bibsched.scripts.bibsched:main',
            'bibstat = invenio.legacy.bibindex.scripts.bibstat:main',
            'bibtaskex = invenio.legacy.bibsched.scripts.bibtaskex:main',
            'bibtasklet = invenio.legacy.bibsched.scripts.bibtasklet:main',
            'bibupload = invenio.legacy.bibupload.scripts.bibupload:main',
            'dbexec = invenio.legacy.miscutil.scripts.dbexec:main',
            'dbdump = invenio.legacy.miscutil.scripts.dbdump:main',
            'docextract = invenio.legacy.docextract.scripts.docextract:main',
            'elmsubmit = invenio.legacy.elmsubmit.scripts.elmsubmit:main',
            'gotoadmin = invenio.modules.redirector.scripts.redirector:main',
            'inveniocfg = invenio.legacy.inveniocfg:main',
            'inveniogc = invenio.legacy.websession.scripts.inveniogc:main',
            'inveniounoconv = invenio.legacy.websubmit.scripts.inveniounoconv:main',
            'oaiharvest = invenio.legacy.oaiharvest.scripts.oaiharvest:main',
            'oairepositoryupdater = invenio.legacy.oairepository.scripts.oairepositoryupdater:main',
            'refextract = invenio.legacy.refextract.scripts.refextract:main',
            'textmarc2xmlmarc = invenio.legacy.bibrecord.scripts.textmarc2xmlmarc:main',
            'webaccessadmin = invenio.modules.access.scripts.webaccessadmin:main',
            'webauthorprofile = invenio.legacy.webauthorprofile.scripts.webauthorprofile:main',
            'webcoll = invenio.legacy.websearch.scripts.webcoll:main',
            'webmessageadmin = invenio.legacy.webmessage.scripts.webmessageadmin:main',
            'webstatadmin = invenio.legacy.webstat.scripts.webstatadmin:main',
            'websubmitadmin = invenio.legacy.websubmit.scripts.websubmitadmin:main',
            'xmlmarc2textmarc = invenio.legacy.bibrecord.scripts.xmlmarc2textmarc:main',
            'xmlmarclint = invenio.legacy.bibrecord.scripts.xmlmarclint:main',
        ],
    },
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite='invenio.testsuite.suite'
)
