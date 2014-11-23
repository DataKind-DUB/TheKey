Textprep
========

Tools for text pre processing.

## Getting Started
This package ships the _textprep_ binary which implements a series of pre-processing steps that execute sequentially on a given input:

```
Usage: textprep [options]

Options:
  -h, --help            show this help message and exit
  --sourcefile=SOURCEFILE
                        File to process.
  --sourcedir=SOURCEDIR
                        Directory to process - will process all files in it.
  --anon-names          Anonymize person names (converts to PERSON)
  --anon-orgs           Anonymize org names (converts to ORGANIZATION)
  --spellcheck          Runs spell corrector
  --verbose             Prints to screen

```
 
## Data
This package uses corpus data from NLTK and word lists from the following sources:
* Apache/Mozilla English dictionary project wordlists: https://github.com/marcoagpinto/aoo-mozilla-en-dict
* CMU names list from: http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/util/areas/nlp/corpora/names/readme.txt
* The US Census names lists: https://www.census.gov/topics/population/genealogy/data/2000_surnames.html

