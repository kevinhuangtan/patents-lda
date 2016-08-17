import logging, gensim, bz2
from gensim import corpora
from os import listdir
from os.path import isfile, join
import glob
from pprint import pprint  # pretty-printer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load txt files from './texts' into array of strings
def load_files():
    path = './texts/*.txt'
    files = glob.glob(path)
    documents = []
    for name in files:
        try:
            with open(name) as f:
                text = f.read()
                documents.append(text)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return documents

# Remove common words (using a stoplist) 
# as well as words that only appear once in the corpus:
def tokenize(documents):
    # remove common words and tokenize
    stoplist = set('for [ ] a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]
    # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    return texts

# id-word mapping
def create_dictionary(texts):
    dictionary = corpora.Dictionary(texts)
    dictionary.save_as_text('./build/dictionary.txt')
    return dictionary

# Vector Space corpus
def create_corpus(texts, dictionary):
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./build/corpus.mm', corpus)  # store to disk, for later use
    return corpus

def prepare_corpus():
    documents = load_files()
    texts = tokenize(documents)
    dictionary = create_dictionary(texts)
    create_corpus(texts, dictionary)



