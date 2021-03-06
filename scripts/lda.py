import logging, gensim, bz2
from gensim import corpora

def run(num_topics, build_path):
	# load id->word mapping (the dictionary), one of the results of step 2 above
	id2word = gensim.corpora.Dictionary.load_from_text(build_path + '/build/dictionary.txt')
	# load corpus iterator
	mm = gensim.corpora.MmCorpus(build_path + '/build/corpus.mm')
	# mm = gensim.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output

	# extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
	# takes ~ 6 hours
	# 1000 passes too much
	# chunksize too small is no good
	lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=num_topics, update_every=1, chunksize=10000, passes=10)

	# wiki model # extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
	# lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=10000, passes=1)


	# print the most contributing words for 20 randomly selected topics
	lda.print_topics(num_topics)
