from setuptools import setup

setup(
    name='tokenize-rt',
    description='A wrapper around the stdlib `tokenize` which roundtrips.',
    url='https://github.com/asottile/tokenize-rt',
    version='2.0.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    py_modules=['tokenize_rt'],
    entry_points={'console_scripts': ['tokenize-rt = tokenize_rt:main']},
)
