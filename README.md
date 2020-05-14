# Conspiracy_Siebe_Project_Specific

**__TBD:__**
I have to incorporate script to incorporate the wordvector + rareterm + neighboring + wordvector dimensions hyperparmaters in my gridsearch (along max features and classifier hypers)

__Info on the files within the repository:__
  - the files that are numbered are subject to be executed within an order i.e. my text classification pipeline; their respective number is their place within that order. Here, the baseline will be set, after the model being optimized in 3Gridsearch(preprocess-vectorizationHyperparametersettings-ClassifierHyperparamaterSettings) 
  
  - the files startin with 'FE'='feature_Enrichment are the core of the feature_engineering process; eventually, their output models will also be input in the TextPipeline from step 3 (GridsearchCV) onwards (to equalize their hyperparamters wit the baseline model): then the results can be compared and the Research Question(RQ)--Can the use of external data improve the performance of a text classification model for detecting conspiratorial video transcripts on a small unbalanced dataset?--can be answered, as the models includes externally derived features, by which the original features are enriched. 
  
  | __file/step__                       | __state__        |
| -------------                     |:-------------:|
| 1_Import+Preprocess.py            |done  | 
| 2.0_vectorization_BOW&split.py    |Gridsearch-system=setup: Hyperparamaters can be optimized (is not crucial for answering RQ, as it is mostly about comparison of models) | 
| 2.5_Analysis.py                   | not relevant for end-result; but I use it for EDA & observing the results of changes in HyperParamaters     |
| 3_GridsearchCV.py                 | Gridsearch-system=setup: Hyperparamaters of baseline classifier can be optimzed even more  |
| FE1_RedditCorpus                  | 'the domain specific external corpus/dataset': 40k reddit comments are scraped, from which feature can be extracted (looking into possibility to use googleBigquery to download an even bigger dataset)
| FE2_FeatureEnrichment             | Working on it; includes a "general corpus": pretrained external wordVector model (GloVe wikipedia 2014 (400k terms) and the code for the feature-enrichment process by which the general & domainspecific corpus (FE2) are input . For these models, vectorization&classifier Hyperparamaters (can(and ought for comparison!) be easily extended here|
