import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def desc():
    info = read('README.md')
    try:
        return info + '\n\n' + read('doc/changelog.rst')
    except IOError:
        return info

setup(
    name='Flask-Hopak',
    version='0.1.0',
    url='https://github.com/xen/flask-hopak',
    license='BSD',
    author='Mikhail Kashkin (@xen), Ilya Petrov (@muromec)',
    description='Admin interface for Flask that uses Hopak models',
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'hopak',
        'Flask-PyMongo',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
