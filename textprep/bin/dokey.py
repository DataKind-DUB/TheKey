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
import cStringIO

def rebuild_poslist(tokens, poslist):
    '''
     rebuilds the pos-tagged list with post-processed tokens list, but preserving tags
    '''
    output = []
    for i in range(len(tokens)):
        output.append((tokens[i], poslist[i][1]))
    return output

def utf8_write(csv_writer, sio, f, record):
    '''
     Gymnastics to make utf-8 work with csv library
    '''
    # first write to string buffer via csv. fields are converted to str
    encoded_recs = [(s if type(s) is str else s.encode('utf-8', errors='replace')) for s in record]
    csv_writer.writerow(encoded_recs)
    # retrieve non utf-8 encoded string from buffer 
    to_file=sio.getvalue()
    # write in "raw" mode
    f.write(to_file)
    sio.truncate(0)

def main():
    # The Key Parameters
    # columns not to be processed 
    IGNORE_COLS=[0,1,3,5]
    IGNORE_SPELL=['beamish', 'quaser', 'wouldnt', 'didnt', 'dont', 'karting', 'center', 'centre', 'xbox', 'bmx', 'havent', 'aswell']
    PREF_WORDS=['deprivation', 'bazaar']

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
    spellchecker=text_util.SpellChecker(ignore_list=IGNORE_SPELL)
    spellchecker.set_preferred_words(PREF_WORDS)

    # readers and writers
    f=open(options.inputcsv, 'rb')
    rd=csv.reader(f)
    fa=open(anonfile, 'wb')
    fc=open(compfile, 'wb')
    fb=open(badfile, 'wb')
    sio_a=cStringIO.StringIO()
    sio_b=cStringIO.StringIO()
    sio_c=cStringIO.StringIO()
    wa=csv.writer(sio_a)
    wc=csv.writer(sio_c)
    wb=csv.writer(sio_b)

    for records in rd:
        print records[0]
        outrecord = [x.decode('utf-8', errors='replace') for x in records]
        if records[0] <> 'groupprojectid':
            # for each selected col, anonymize and generate output record
            try:
                for i in [i for i in range(len(records)) if i not in IGNORE_COLS]:
                    # convert to utf-8
                    this_rec=records[i].decode('utf-8', errors='replace')
                    tokens = nltk.word_tokenize(this_rec)
                    pos_tokens = nltk.pos_tag(tokens)
                    # step 1 - spell check
                    tokens = spellchecker.correct_tokens(tokens, pos_tokens)
                    pos_tokens = rebuild_poslist(tokens, pos_tokens)
                    # step 2 - orgs
                    tokens = org_an.anonymize_tokens(tokens, pos_tokens, anonstr='XXXX')        
                    pos_tokens = rebuild_poslist(tokens, pos_tokens)
                    # step 3 - names
                    tokens = names_an.anonymize_tokens(tokens, pos_tokens, anonstr='XXXX')
                    outrecord[i] = ' '.join(tokens)
            except Exception,e:
                print 'Unable to load %s - %s' % (records[0], str(e))
                utf8_write(wb, sio_b, fb, records)
                continue

        # write output record
        # csv library does not have support for utf-8, so we write directly to the file via stringIO conversion
        # https://docs.python.org/2/library/csv.html#csv-examples
        utf8_write(wa, sio_a, fa, outrecord)
        # builds a list of pairs from anonymized and non anonymized csvs, write comparison csv
        temprecord = [(records[i], outrecord[i]) for i in range(len(records))]
        comprecord = []
        for tup in temprecord:
            comprecord += [tup[0], tup[1]]
        utf8_write(wc, sio_c, fc, comprecord)

# Main
if __name__=='__main__':
    main()
