#!/usr/bin/env python
# coding: utf-8

import re
import nltk
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.under_sampling import RandomUnderSampler

nltk.download('stopwords')
nltk.download('rslp')
stopwords = nltk.corpus.stopwords.words('portuguese')
stemmer = nltk.stem.RSLPStemmer()

def remove_noise(text):
    
    text = text.replace('-', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\\', '')
    text = text.replace('*', ' ')
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\b\w\b', ' ', text)
    text = re.sub(r"[()`#/@';:%<>$&\"{}~+=?|]", " ", text)
    text = re.sub(' +', ' ', text)
    
    return text

def stemming(text):
    
    tokens = text.split(" ")
    
    aux = []
    for i in tokens:
        try:
            aux.append(stemmer.stem(i))
        except:
            continue

    text = " ".join(aux)
    
    return text

def tf_idf(X):
    
    tfidf =TfidfTransformer(norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
    data =tfidf.fit_transform(X)
    
    return data.todense()


def balance_data (X, y,random_state=42):
    
    rus = RandomUnderSampler(random_state=random_state)
    X, y = rus.fit_resample(X, y)
    
    return X, y
