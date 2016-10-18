from scripts import prepare_corpus
from scripts import lda
import timeit


# FIRST run : pg_ctl -D /Volumes/KLJ-DATA-03/postgres start

start = timeit.timeit()
print "start time"

build_path = '/Volumes/KLJ-DATA-03'

# STEP 1: Prepare corpus
print 'prepare corpus'
prepare_corpus.run(build_path)

# STEP 2: Run LDA
NUM_TOPICS = 100
print 'run lda'
z = lda.run(NUM_TOPICS, build_path)

end = timeit.timeit()
print end - start