from scripts import prepare_corpus
from scripts import lda

# STEP 1: Prepare corpus
prepare_corpus.run()

# STEP 2: Run LDA 
z = lda.run()
