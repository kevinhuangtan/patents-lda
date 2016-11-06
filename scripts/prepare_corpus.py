import logging, gensim, bz2
from gensim import corpora
from os import listdir
from os.path import isfile, join
import glob
from collections import defaultdict
from pprint import pprint
import re, string
from nltk.stem import *
from nltk.stem.porter import *
# -*- coding: utf-8 -*-

# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH

def print_newline():
    print '_______________________\n\n'
    return

import psycopg2
import sys
import xml.etree.ElementTree as ET

def xml_to_text(xml):
    body = xml[0] # extract tuple
    body_no_xml = re.sub('<[^>]*>', '', body)
    return body_no_xml

def pg_query():

    conn_string = "host=localhost port=5432 dbname=rpx user=kljensen"
    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # execute our Query
    cursor.execute("set search_path TO core;")
    cursor.execute("SELECT description FROM pat_descriptions LIMIT 100000")

    # # retrieve the records from the database
    return [xml_to_text(record) for record in cursor]


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load txt files from path into array of strings
# txt file should have each document on new line
def load_text():
    documents = pg_query()
    return documents

def clean_word(word):
    table = string.maketrans("","")
    word = word.translate(table, string.punctuation) # remove punctuation
    word =  re.sub(r'[^\x00-\x7f]',r'', word)  # remove non Ascii
    return word

def apply_stoplist(word):
    # remove common words and tokenize
    stoplist_string = """ 
        for [ ] a of the 
        by and to in is an be with or at can that are than each from as about which with on 
        from after was when were this such may it me if not fig. has no into any these one other
        will then use
        """ 

    stoplist = set(stoplist_string.split())

    if(word in stoplist):
        return False
    if(word.isdigit()):
        return False
    return True 

# Remove common words (using a stoplist)
# as well as words that only appear once in the corpus:
def tokenize(documents):
        # texts = [[clean_word(word) for word in document.lower().split() if apply_stoplist(word)]
        #      for document in documents]
    print 'create bag of words'
    texts = []
    for i in range(0, len(documents)):
        print 'doc #', i
        document = documents[i]
        words = [clean_word(word) for word in document.lower().split() if apply_stoplist(word)]
        stemmer = PorterStemmer()
        words_stemmed = [stemmer.stem(word) for word in words]
        texts.append(words_stemmed)

    print 'remove unique words'
    # remove words that appear only once
    frequency = defaultdict(int)
    texts_num = 0
    for text in texts:
        print 'doc #', texts_num
        texts_num += 1
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    return texts

# id-word mapping
def create_dictionary(texts, build_path):
    dictionary = corpora.Dictionary(texts)
    dictionary.save_as_text(build_path + '/build/dictionary.txt')
    return dictionary

# Vector Space corpus
def create_corpus(texts, dictionary, build_path):
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(build_path + '/build/corpus.mm', corpus)  # store to disk, for later use
    return corpus

def run(build_path):
    print 'loading docs'
    documents = load_text()

    print 'tokenizing'
    
    texts = tokenize(documents)
    print 'building dictionary'

    dictionary = create_dictionary(texts, build_path)
    print 'creating corpus'

    create_corpus(texts, dictionary, build_path)
    return
