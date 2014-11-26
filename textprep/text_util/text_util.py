###
#
# text_util
#
# text processing library for anonymization and spelling
#
###

import nltk
import os

class TextProcessor(object):
    '''
      Generic anonymizer text. Subclass this to implement a specific text anonymization algorithm
    '''
    def __init__(self):
        curpath = os.path.dirname(os.path.abspath(__file__))
        self.stopword_file=os.path.join(curpath,'data/objective.txt')
        self.stopwords = self._get_names_lookup(self.stopword_file)
        self._ANON_TAGS = ['PERSON', 'ORGANIZATION']

    def sanitize(self, token):
        '''
         basic cleanup of input strings - converts to lowercase, removes unwanted stuff
        '''
        return token.lower().replace(' ','').replace('\n','').replace('\r','').replace('\t','')

    def _get_names_lookup(self, filename='names.txt'):
        '''
         Loads a list of names list into a hash lookup (set)
        '''
        names=set([])
        f=open(os.path.join(os.path.curdir, filename))
        for name in f.readlines():
            sanename=self.sanitize(name)
            names.add(sanename)
        return names
    
    def is_stopword(self, token):
        return token in self.stopwords


class OrgAnonymizer(TextProcessor):
    '''
     Anonymyzes organization names with Named Entity Chunking
    '''
    def __init__(self):
        super(OrgAnonymizer, self).__init__()

    def anonymize_tokens(self, inputlist, pos_taglist=None, anonstr='ORGANIZATION'):
        '''
         Takes input list of tokens (and optional pos_tagged list) and replaces ocurrences of  organization names with anonstr argument.

         This algorithm scans tokens for named entities using nltk's ne_chunk()
        '''
        
        # POS-tag input tokens if not already given
        if not pos_taglist:
            pos_taglist=nltk.pos_tag(inputlist)

        # Generate chunk tree and list of named entity candidates
        chunktree=nltk.ne_chunk(pos_taglist)
        ne_candidates = [t for t in chunktree.subtrees() if t.label()=='ORGANIZATION']
        # first anonymizes pos-tagged list with matching chunks
        for node in ne_candidates:
            for tuple_index in range(len(node.leaves())):
                # replaces tree item with anonymized entry
                (t_token, t_pos)=node.leaves()[tuple_index]
                # to avoid confusion on anynomization pipelines, we check against already anonymized content
                if t_token not in self._ANON_TAGS:
                    node.remove((t_token, t_pos))
                    node.insert(tuple_index, (anonstr, t_pos))
 
        # Now tree has anonymized organizations. returns flattened version
        # now returns original list with anonymized tokens
        return [token for (token, pos) in chunktree.flatten().leaves()]
        
 
class NamesAnonymizer(TextProcessor):
    '''
      Anonymizer for surnames and given names based on word lists. 

      This algorithm uses word lists obtained from:
      1/ CMU's word list from:
         http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/util/areas/nlp/corpora/names/readme.txt

      2/ The US Census word lists
         https://www.census.gov/topics/population/genealogy/data/2000_surnames.html
    '''
    def __init__(self):
        super(NamesAnonymizer, self).__init__()
        curpath = os.path.dirname(os.path.abspath(__file__))
        self.frequent_names_file='data/cmu_names.txt'
        self.all_names_file='data/names_all.txt'
        self.all_names=self._get_names_lookup(os.path.join(curpath, self.all_names_file))
        self.freq_names=self._get_names_lookup(os.path.join(curpath, self.frequent_names_file))

    def sanitize(self, token):
        '''
          Performs generic token "sanitization", also taking care of converting O'Surname -> OSurname (per input text file) 
        '''
        return super(NamesAnonymizer, self).sanitize(token).replace("'",'')

    def anonymize_tokens(self, inputlist, pos_taglist=None, anonstr='PERSON'):
        '''
          Rule based anonymization of person names. Replaces found ocurrences with anonstr argument
          This algorithm uses part-of-speech and chunking information and a word list as follows:
          - names POS-tagged as NN* 
          AND
          - NOT a stopword
          AND
            - matching a term in the high frequency list AND not lexicalized term in WN.
            OR
            - NNP tag and matches full names list AND not lexicalized term in WN
            OR
            - NNP tag and matches high freq list

          Returns a list of tokens with results of anonymization.
        '''
        wnl=nltk.stem.WordNetLemmatizer()
        outputlist = []
        # POS-tag input tokens if not already given
        if not pos_taglist:
            pos_taglist=nltk.pos_tag(inputlist)

        # Generate chunk tree and list of named entity candidates
        chunktree=nltk.ne_chunk(pos_taglist)
        ne_candidates = []
        for c in [t.leaves() for t in chunktree.subtrees() if t.label()=='PERSON']:
            ne_candidates += c

        for (token, pos) in pos_taglist:
            outtoken = token
            lemma=wnl.lemmatize(self.sanitize(token))
            if ('NN' in pos) and (not self.is_stopword(lemma)):
               # Rule 1: tagged NN*, not a dictionary word and present in high freq names list
               if (not nltk.wordnet.wordnet.synsets(lemma, pos='n')) and (lemma in self.freq_names):
                   print '[anonymizer] rule 1: replacing '+lemma
                   outtoken=anonstr
               # Rule 2: tagged as NNP and in list of all names
               elif (pos == 'NNP') and (not nltk.wordnet.wordnet.synsets(lemma, pos='n')) and (lemma in self.all_names):
                   print '[anonymizer] rule 2: replacing '+lemma
                   outtoken=anonstr
               # Rule 3: NNP and high frequency names - dont care if its lexicalized, just trust it
               elif (pos == 'NNP') and (lemma in self.freq_names):
                   print '[anonymizer] rule 3: replacing '+lemma
                   outtoken=anonstr
               # Rule 4: in NE list and present in names list
               elif ((token, pos) in ne_candidates) and (not nltk.wordnet.wordnet.synsets(lemma, pos='n')) and (lemma in self.all_names):
                   print '[anonymizer] rule 4: replacing '+lemma
                   outtoken=anonstr
            outputlist.append(outtoken)

        return outputlist



##
#
# Spelling
#
##
class SpellChecker(TextProcessor):
    '''

      Uses word lists from NLTK and a spell checker algorithm described in:
      https://github.com/mattalcock/blog/blob/master/2012/12/5/python-spell-checker.rst

      In the future this may support pyenchant or another core library with better functionality.
    '''
    
    def __init__(self, wordlistfile=None, ignore_list=[]):
        self.alphabet='abcdefghijklmnopqrstuvwxyz'
        self.wordlist=self._load_wordlists(wordlistfile)
        # prepare freq dist data, use gutemberg corpus
        gut=nltk.corpus.gutenberg.words()
        self.freqdist=nltk.FreqDist(w.lower() for w in gut)
        # ignore lists
        self.IGNOREPOS=set(['NNP', '.', ',', ':', 'CD'])
        self.IGNORETOKENS=set(["n't", "'s", "'d", "'ve", "'ll", "'nt", "'", "&", "n/a", "etc", "na",
                                 "tbc", "tbd", "tba"])
        if ignore_list: self.IGNORETOKENS = self.IGNORETOKENS.union(set(ignore_list))

        # a lemmatizer
        self.wnl=nltk.wordnet.WordNetLemmatizer()

    def _load_wordlists(self, wordlistfile=None):
        '''
         Load wordlists from nltk corpora and apache project
        '''
        curpath = os.path.dirname(os.path.abspath(__file__))
        if not wordlistfile:
            wordlistfile=os.path.join(curpath, 'data/apache_wordlist.txt')

        words_set = self._get_names_lookup(wordlistfile)
        return words_set


    def is_word(self, word):
        '''
         boolean - do we know about this word?
        '''
        return self.sanitize(word) in self.wordlist

    def edits(self, word):
        '''
         Given an input word, returns a set of possible edit operations derived from it
         See: https://github.com/mattalcock/blog/blob/master/2012/12/5/python-spell-checker.rst
        '''
        # s is all possible slicings of this word
        s=[(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes=[a + b[1:] for a, b in s if b]
        transposes=[a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
        replaces=[a + c + b[1:] for a, b in s for c in self.alphabet if b]
        inserts=[a + c + b for a, b in s for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)


    def suggest(self, word, limit=5):
        '''
          returns list of suggestions based on input word permutations
        '''
        suggested = []
        # take care of dummy case
        if self.is_word(word):
            suggested.append(word)
        # now check which permutations e know of, compile list of tuples (found word, frequency)
        found_words=[(w, self.freqdist.freq(w)) for w in self.edits(self.sanitize(word)) if w in self.wordlist]
        # sort this list by frequency of ocurrence
        found_words.sort(key=lambda x:x[1], reverse=True)
        suggested += [w[0] for w in found_words]
        # now cap at word limits
        return suggested[:limit]

    def _is_candidate(self, word, pos):
        '''
         boolean that determines if word/pos pair is a candidate for spell checking, based on current ignore rules and
         word list to ignore.

         Evaluates as follows:
         - not in ignore list
         - pos not in ignore list (punctuations, NNP, CD)
         - not capitalized
         - not in dictionary
         - only alphabet words
         - > 1 chars
        '''
        return (pos not in self.IGNOREPOS) and len(word)>2 and (word not in self.IGNORETOKENS)\
               and word.isalpha() and not word.istitle() and not word.isupper()\
               and not self.is_word(self.wnl.lemmatize(word))

    def correct_tokens(self, inputlist, pos_taglist=None):
        '''
         Given a list of input tokens, runs spell checker auto-correcting mistakes
        '''
        # POS-tag input tokens if not already given
        if not pos_taglist:
            pos_taglist=nltk.pos_tag(inputlist)
       
        outtokens = []
        for (token, pos) in pos_taglist:
            if self._is_candidate(token, pos):
                suggestions=self.suggest(token)
                if suggestions:
                    outtokens.append(suggestions[0])
                    print '[spellchecker] Replacing %s with %s' % (token, suggestions[0])
                else:
                    outtokens.append(token)
            else:
                outtokens.append(token)

        return outtokens
