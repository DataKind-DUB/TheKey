'''
  setup.py for textprep - text processing module
'''
from distutils.core import setup

setup(
    name='Textprep',
    version='0.5.dev',
    author='Bruno Ohana',
    author_email='bohana@gmail.com',
    packages=['text_util'],
    package_data={'text_util': ['data/*.dat', 'data/*.txt']},
    scripts=['bin/textprep', 'bin/get_names.sh', 'bin/dokey.py'],
    url='https://github.com/DataKind-DUB/TheKey',
    license='MIT',
    description='Toolkit for text preparation activities: anonymization, spell checking, etc.',
    long_description=open('README.md').read(),
    install_requires=[
        "nltk >= 3.0.0"
    ],
)
