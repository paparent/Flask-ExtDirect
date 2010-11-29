"""
Flask-ExtDirect
---------------

Adds Ext.Direct support to Flask. Under development.

Links
`````

* `documentation <http://packages.python.org/Flask-ExtDirect>`_
* `development version
  <http://github.com/paparent/Flask-ExtDirect/zipball/master#egg=Flask-ExtDirect-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-ExtDirect',
    version='0.1',
    url='http://github.com/paparent/Flask-ExtDirect/',
    license='MIT',
    author='PA Parent',
    author_email='paparent@paparent.me',
    description='Adds Ext.Direct support to Flask.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
