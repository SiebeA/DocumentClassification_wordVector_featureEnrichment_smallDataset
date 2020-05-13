#
## =============================================================================
## Importing libraries
## =============================================================================
##nlp essentials:



import en_core_web_sm # the english spacy core (sm = small database)
# for installing spacy & en_core; https://spacy.io/usage

# wordvec (GloVe) model:
import numpy as np
#%matplotlib notebook
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec#pretrained on wiki2014; 400kTerms

#loading the word vectors
GLOVE_FILE = datapath("C:\\Users\\Sa\\Google_Drive\\0_Education\\1_Masters\\WD_jupyter\\wordVectors\\glove.6B.50d.txt")
WORD2VEC_GLOVE_FILE = get_tmpfile("glove.6B.50d.txt") # specify which d file is used here
glove2word2vec(GLOVE_FILE,WORD2VEC_GLOVE_FILE)

#model:
model = KeyedVectors.load_word2vec_format(WORD2VEC_GLOVE_FILE)



# ***run from here, information for understanding is provided in the print commands ***

#======================================================================== #
''' 3 Creating the toy corpus    '''
#======================================================================== #
STRING = '''chinese beijing
chinese chinese shanghai macao
chinese macao japan shanghai
tokyo japan chinese
japan hiroshima hiroshima'''
# side-obervation: Macau in doc 3 is the most informative word IDF


#define labels because I want to add them to the df
γTrain = ['chinese' , 'chinese' ,'chinese' , 'japanese']
    
#STRING2 = '''I've been to Hollywood and redwood
#I've been to Redwood
#I've been a miner for a heart of gold'''

Toy_corpus = STRING.splitlines()
    

## experiment with n-gram model
#def ngrams(words, n=2):
#    for idx in range(len(words)-n+1):
#        yield tuple(words[idx:idx+n])
#for ngram in ngrams(Toy_corpus, n=1):
#    print(ngram)
#    
#x = ngrams(Toy_corpus)



import en_core_web_sm
nlp = en_core_web_sm.load(disable=["tagger", "parser", "ner"]) #DISABLE NER IF NOT NECESSARY, LOTS OF MEMORY REQUIREMENTS


def my_cleaner4(text):
        return[token.lemma_ for token in nlp(text) if not (token.is_stop or token.is_alpha==False or len(token.lemma_) <3) ]
        
#to see which words are filtered out because they are stop words:
#from spacy.lang.en.stop_words import STOP_WORDS

#creating a token counts vectorizer:
    # Convert a collection of text documents to a matrix of token counts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer




# =============================================================================
'4 Creating a term-document-Matrix FITTING THE VECTORIZER   '
# =============================================================================
vectorizer=TfidfVectorizer(tokenizer=my_cleaner4)
print(f'the vectorizer has been created, and it specifically involves a:\n      {str(type(vectorizer))[-17:-2]}')
print('\n fitting the vectorizer by inputing the corpus...')
tdm = vectorizer.fit_transform(Toy_corpus)
print('\n the vectorizer has been fit')
Tdm_array = tdm.toarray()
##ngrams:
#vectorizer_Ngram = CountVectorizer(ngram_range=(2,2),tokenizer=my_cleaner4)
#tdm_nGram=vectorizer_Ngram.fit(toy_corpus)
#print (tdm_nGram.get_feature_names()  )
#terms_bigrams = tdm_nGram.get_feature_names()
    
#terms:
Terms = vectorizer.get_feature_names()
print(f'size of Vocabulary = {len(Terms)}\n')



# terms+TFIDF in df:
import pandas as pd

TermsψcountValues = pd.DataFrame(Tdm_array,columns=Terms,index=['doc0(chi) WC:','doc1(chi) WC:','doc2(chi) WC:','doc3(jap) WC:','doc4(jap) WC:']) #deprecated, further along the script you have: 




# =============================================================================
# 
# =============================================================================
#termsψcoefsψcountvalues # SO THAT I DONT forget; define this in section 6


# =============================================================================
' 5 machine learning'
# =============================================================================

γTrain = ['chinese' , 'chinese' ,'chinese' , 'japanese']
#import numpy as np
#LabelsNumeric = np.array((1,0,0))
    
#train/test subset
import numpy as np
χTrainVec =  np.array( TermsψcountValues.iloc[[0,1,2,3]] )


# =============================================================================
# Multinominal Naive Bayes MNB
# =============================================================================
from sklearn.naive_bayes import MultinomialNB
#mnb_model=MultinomialNB() # ~==↓
mnb_model= MultinomialNB(alpha= 0.1, fit_prior = True, class_prior = (0.5,0.5) ) # apt the order of which class_prior paramters, are the order of: mnb_model.classes_


print (f'\n mnb_model.class_prior is specified as: {mnb_model.class_prior}... ') # this works before fitting
mnb_model.fit(χTrainVec, γTrain)
print ('which results in a class prior of: ', np.exp(mnb_model.class_log_prior_  ) ) # this only works after fitting
print('\n respecively for the classes:',mnb_model.classes_)
# use the EXP (invese log / euler) to convert the log back to probabilities:

# =============================================================================
'6 ANALYZING section; how the learnignAlgorithm works   '
# =============================================================================

TermsAKAfeatures = vectorizer.get_feature_names()
TermsWcoefs = pd.DataFrame(pd.DataFrame(np.exp(mnb_model.coef_),columns= TermsAKAfeatures,index=['coefs'])).round(2) #converting logs to probabilites by exp()

print ( f'the number of features: {mnb_model.n_features_} == size of vocabulary == nr of terms\n\n the terms/features and their coefs:\n{TermsWcoefs}') #how many features there are: 6 terms


#conditional probabalities AKA likelihoods
# answers the question: what is the probability of the word ... 'beijng' given that the class is chinese, or given that the class is japanese
TermsψconditionalProbs =pd.DataFrame(np.exp(mnb_model.feature_log_prob_),columns=TermsAKAfeatures,index=['prob|chinese','prob|japanese']) 


print(f'\n\n this leads to the following probabilities of a particular TERM (dependent) being encountered GIVEN THE OBSERVATION of the CLASS (causal) Chinese or Japanese: \n load (**TermsψconditionalProbs**) in VE: ....\n intuitively the probs makes sense, e.g. as when the class "japanese" is encountered the prbobability that the word "tokyo" will be encountered given japanese is larger than if the given is chinese.\n\n' )

# =============================================================================
# PULL UP IN VE for clear overviews:
# =============================================================================
termsψcoefsψcountvaluesψconditionalProbs = pd.concat([TermsWcoefs, TermsψcountValues,TermsψconditionalProbs ] , axis=0).round(2) #neatly in 1 df
print(termsψcoefsψcountvaluesψconditionalProbs, '\n\n ↑termsψcoefsψcountvaluesψconditionalProbs')
#analysis:
# the coefs for a word are the same as the probabilities of that word occuring, if the other class is observed
 



#!!!======================================================================== #
'Recreating HEAP METHOD for Enriching BOW        '
#======================================================================== #


'''                 Description of method:
test data →→→ 
wordVec model finds neighbors if term in testset is Rare⊃outOfVocab → 
construct new BOW vector where neigbors are +1, other terms untouched →  
'''
# =============================================================================
# Scenario in which the baseline model is used: no intermediate wordvector model:
# =============================================================================

                            
rare_test = '''beijing chinese japan hiroshima
chinese bejing macao tokyo'''.splitlines()                            
# SO IF THIS TEST-VECTOR INCLUDING BEIJING, WHICH HAS NEIGHBOR: 'SHANGHAI' IS ENRICHED WITH SHANGHAI; IT WLL BE HEAVILY PROBABILITIZED TOWARDS CLASS=CHINESE; DOES THAT SEEM JUSTIFIED?:
    # IF EG SHANGHAI IS NOT PRESENT IN THE TEST_VECTOR, AND THAT TERM IS VERY CLOSE TO A TERM IN THE  TEST SET THAT IS A RARE TERM FOR THAT CLASS THUS COUNTING LITTLE TOWARDS THE PROBABILITY TOWARDS THAT CLASS; ONE COULD SAY THAT IN ACTUALITY THAT TERM IS SORT OF A PLACEHOLDER FOR THE NEIGHBORING=SIMILAR TERM THAT DOES OCCUR MANY TIMES IN THAT CLASS, LITTLE IN OPPOSING CLASS THEREFORE PROVIDING A LOT OF EVIDENCE FOR THE TEST-TEXT BEING CLASSIFIED AS THAT CLASS
    # EXPLANATION WH IT MATTERS FOR OUTCOME: tHE MORE COMMON SHANGHAI IS IN CHINESE CLASSES |\ MORE RARE IN JAPANESE CLASSES; THE HIGHER THE LIKELIHOOD FOR CLASS CHINESE &_BY_DEF?: THE LOWER THE LIKELIHOOD FOR CLASS JAPANUSE →→→ HENCE THE GREATER THE "PROBABILITY GAP" BETWEEN THAT WORD COUNTING TOWARDS CHINESE VS JAPANESE

# =============================================================================
# Scenario before enrichment:
# =============================================================================
x_test = vectorizer.transform(rare_test).toarray()

ŷ = mnb_model.predict(x_test) #  the predicted class
print('the predicted classes:',ŷ)
ŷ_probability = mnb_model.predict_proba(x_test)
print('\n\nwith the probabilities for the respective docs:\n',ŷ_probability)
print ('\n\n with the para:', mnb_model)
#i.e. terms that do not occur in the (training)vocab are discarded by the classifier


#!!!=============================================================================
#Enriching the Rare and out of vocab words:
#I NOW FORMULATED A MINIMUM SIMILARIT SCORE (NOT SAME AS HEAP)
# ============================================================================

#model.similar_by_word('hiroshima', topn= 40)

#PROTOTYPE 2
df = termsψcoefsψcountvaluesψconditionalProbs.iloc[1:6]
df_test = pd.DataFrame(x_test,columns=vectorizer.get_feature_names()) #test df
df_enriched = df_test.replace(df_test, 0) #creating the (here) empty enriched BOW

import time
START_TIME = time.time()

for DOCINDEX in range(len( df_test)): # loops through each of the docs
    print(DOCINDEX)
    for TERM in df_test: #loops through each of the terms, of each of the doc
#        print(TERM)
        if df_test.iloc[DOCINDEX][TERM]>0 and np.count_nonzero(df[TERM]) <= 1: #checks how many non0/occurences the term has along all docs in training
            print(f'\n "{TERM}" satisfies the "rare word paramater"')
            
            for NEIGHBOR in model.similar_by_word(TERM, topn= 10): #SET 'K' NEIGHBORs HYPERPARAMATER
                if NEIGHBOR[1]>0.8 and NEIGHBOR[0] in df.columns:

                    print(f'TERM:{TERM} \n NEIGHBOR:{NEIGHBOR[0]} with a similarity of {NEIGHBOR[1]}')
                    df_enriched.iloc[DOCINDEX][NEIGHBOR[0]] += NEIGHBOR[1] * df_test.iloc[DOCINDEX][TERM]  #adding a value that is the product of the similarity score * the value of the TERM in the respective DOC, to the NEIGHBOR of the rare term in the DOC where the rare term occurs: 


                    
# #observing some stuff
# =============================================================================
#EnrichTime = time.time() - START_TIME # this is all ← ↓3  to observe how much longer it takes for changes
#print(f'time it took {EnrichTime}')
#Comparetime = EnrichTime 
#EnrichTime / Comparetime
#
#model.similar_by_word("beijing", topn= 10)
# =============================================================================

#observing the dataframe results as result of enrichment
#print('\n test df \n',df_test,'\n',)

print('\n df enriched df \n',df_enriched,'\n',)

df_aggregated = df_test+df_enriched
print('\n aggregated df \n',df_aggregated,'\n',)

df_difference = df_aggregated-df_test
print('df difference:\n',df_difference)



# =============================================================================
# TBD: multiple text docs , and with how many words should I increase the neighbors? (1 for every term use of the TERM?)
# =============================================================================


# =============================================================================
# Scenario of classifing with enrichment:
# =============================================================================
print()
ŷ = mnb_model.predict(df_aggregated) #  the predicted class
print(ŷ)
ŷ_probability = mnb_model.predict_proba(df_aggregated)
print(ŷ_probability)
print ('\n\n with the para:', mnb_model)