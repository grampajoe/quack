from setuptools import setup

setup(
    name='quack',
    description='Mock and SQLAlchemy but not horrible.',
    url='https://github.com/grampajoe/quack',
    version='0.0.1',
    author='Joe Friedl',
    author_email='joe@joefriedl.net',
    py_modules=['quack'],
    install_requires=[
        'SQLAlchemy==0.7.9',
        'mock==1.0.1'
    ]
)
