#!/bin/env python

#
# Script to anonymize the key's csv.
# Generates .anon.csv containing anoymized entries
# Generates .comp.csv containing pre and post anonymization for comparisons
# Generates .bad.csv containing entries that failed processing for later inspection
#
import csv
import text_util
import nltk
from optparse import OptionParser

def rebuild_poslist(tokens, poslist):
    '''
     rebuilds the pos-tagged list with post-processed tokens list, but preserving tags
    '''
    output = []
    for i in range(len(tokens)):
        output.append((tokens[i], poslist[i][1]))
    return output

def main():
    # columns not to be processed 
    IGNORE_COLS=[0,1,3,5]

    mainparser=OptionParser()
    mainparser.add_option('--inputcsv', action='store', type='string', default='groupprojectfreetext.csv', dest='inputcsv',
        help='CSV File to process.')
    (options, args)=mainparser.parse_args()

    # output files generated
    anonfile=options.inputcsv + '.anon'
    compfile=options.inputcsv + '.comp'
    badfile=options.inputcsv + '.bad'

    # Generate anonymizers
    print 'Loading anonymizers...'
    names_an=text_util.NamesAnonymizer()
    org_an=text_util.OrgAnonymizer()

    # manually excludes some domain words and some problems it cant figure out on its own
    spellchecker=text_util.SpellChecker(ignore_list=['deprevation','quaser','wouldnt','didnt','dont','karting','center','centre','quaser'])

    # readers and writers
    f=open(options.inputcsv)
    rd=csv.reader(f)
    fa=open(anonfile, 'w')
    fc=open(compfile, 'w')
    fb=open(badfile, 'w')
    wa=csv.writer(fa)
    wc=csv.writer(fc)
    wb=csv.writer(fb)

    for records in rd:
        print records[0]
        outrecord = [x for x in records]
        if records[0] <> 'groupprojectid':
            # for each selected col, anonymize and generate output record
            outrecord = [x for x in records]
            try:
                for i in [i for i in range(len(records)) if i not in IGNORE_COLS]:
                    tokens = nltk.word_tokenize(records[i])
                    pos_tokens = nltk.pos_tag(tokens)
                    # step 1 - spell check
                    tokens = spellchecker.correct_tokens(tokens, pos_tokens)
                    pos_tokens = rebuild_poslist(tokens, pos_tokens)
                    # step 2 - orgs
                    tokens = org_an.anonymize_tokens(tokens, pos_tokens, anonstr='XXXX')        
                    pos_tokens = rebuild_poslist(tokens, pos_tokens)
                    # step 3 - names
                    tokens = names_an.anonymize_tokens(tokens, pos_tokens, anonstr='XXXX')
                    # put it back together and save
                    outrecord[i] = ' '.join(tokens)
            except Exception,e:
                print 'Unable to load %s - %s' % (records[0], str(e))
                wb.writerow(records)
                continue

        # write output record
        wa.writerow(outrecord) 
        # builds a list of pairs from anonymized and non anonymized csvs, write comparison csv
        temprecord = [(records[i], outrecord[i]) for i in range(len(records))]
        comprecord = []
        for tup in temprecord:
            comprecord += [tup[0], tup[1]]
        wc.writerow(comprecord)

# Main
if __name__=='__main__':
    main()
