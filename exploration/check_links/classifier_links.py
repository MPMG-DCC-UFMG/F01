# -*- coding: utf-8 -*-
# +
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_auc_score, f1_score

from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import model_selection

from imblearn.under_sampling import RandomUnderSampler

import nltk
nltk.download('stopwords')
nltk.download('rslp')
stopwords = nltk.corpus.stopwords.words('portuguese')
stemmer = nltk.stem.RSLPStemmer()


# -

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


def format_targets():
    
    targets_for_text = ['câmara', 'legislativo', 'controladoria-geral', 'plurianual', 'despesas',
                   'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                   'convênios', 'viagens', 'concurso', 'contas públicas', 'obras públicas',
                   'portal da transparência', 'transparência']
    
    #targets_for_text = [stemmer.stem(i) for i in targets_for_text]
    targets = '|'.join(targets_for_text)
    
    return targets, targets_for_text


def pontuar_texto(text, targets):
    
    find = re.findall(targets, text)
    
    return find

def pontuar_os_municipios(df, targets):

    count = 0
    for municipio in df.loc[:, 'Município']:
        name = 'portais/' + str(count) + '.html'
        
        try:
            with open(name, 'r') as arq:
                
                page = arq.read()
                text = BeautifulSoup(page, "html5lib").get_text().lower()
                
                #if text != '':
                #    text = remove_noise(text)
                #    text = stemming(text)
                    
                if len(text) < 300:
                    df.loc[count, "consegui_html"] = 0
                else: 
                    df.loc[count, "consegui_html"] = 1

                portal_estadual = re.findall('portaltransparencia.gov.br', df.loc[count, 'Portal da Transparência'])
                if portal_estadual:
                    df.loc[count, "consegui_html"] = None

                find_targets = pontuar_texto(text, targets)
                for palavra in find_targets:
                    df.loc[count, palavra] += 1
            count += 1
        except IndexError:
            count += 1
            continue
        except FileNotFoundError:
            count+=1
            continue
    return df


def prepare_dataset(df, train=True):
    
    df['Link Correto'] = df['Link Correto'].replace(['x'], 1)
    df['Link Correto'].fillna(0, inplace=True)
    
    df.loc[:, "consegui_html"] = None
    
    targets, targets_for_text = format_targets()
    
    df[targets_for_text] = 0
    
    df = pontuar_os_municipios(df, targets)

    df = df.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    if train:
        df = df.loc[ : 301, :]
        df = df.dropna(subset=['consegui_html'])
    
    result_search = df['consegui_html']
    del df['consegui_html']
    
    return df, result_search


def plot_dtc(classifier, feature_names):
    
    fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
    plot_tree(classifier,
            filled = True,
            feature_names=feature_names);
    fig.savefig('imagename.png')


def cross_validation(model, X_train, y_train):
    
    kfold = model_selection.KFold(n_splits=10)
    results = model_selection.cross_val_score(model, X_train, y_train.ravel(), cv=kfold)
    print("Accuracy: %.3f%% (%.3f%%)" % (results.mean()*100.0, results.std()*100.0))


def fit_dtc(
    X_train, y_train, criterion='gini', min_samples_leaf=1, min_samples_split=2,
    max_depth=None, splitter='best', random_state=None):
    
    classifier = DecisionTreeClassifier(
        criterion=criterion, min_samples_leaf= min_samples_leaf,
        min_samples_split=min_samples_split, max_depth=max_depth,
        random_state=random_state)
    
    classifier.fit(X_train, y_train.ravel())
    
    return classifier


def predict(model, X_test, y_test, verbose=True):

    y_pred = model.predict(X_test)
    
    if verbose:
        print("Consusion Matrix: \n{}".format(confusion_matrix(y_test, y_pred)))
        print("Accuracy: {}".format(accuracy_score(y_test, y_pred)))
        print("Precision: {}".format(precision_score(y_test, y_pred)))
        print("Recall: {}".format(recall_score(y_test, y_pred)))
        print("F1-score: {}".format(f1_score(y_test, y_pred)))

    return y_pred


def grid_search(parameters, model, X_train, y_train):
    
    gsearch = GridSearchCV(model, parameters)
    gsearch.fit(X_train, y_train.ravel())
    
    return gsearch


def randomized_search (parameters, model, X_train, y_train):
    
    rsearch = RandomizedSearchCV(estimator=model, param_distributions=parameters, n_iter=100)
    rsearch.fit(X_train, y_train.ravel())
    
    return rsearch


def test_parameters(X_train, y_train, classifier, parameters, search_model='rsearch', verbose=True):
    
    if search_model == 'gsearch':
        search = grid_search(parameters, classifier, X_train, y_train)
    elif search_model == 'rsearch':
        search = randomized_search (parameters, classifier, X_train, y_train)
        
    if verbose:
        print('criterion: {}'.format(search.best_estimator_.criterion))
        print('splitter: {}'.format(search.best_estimator_.splitter))
        print('min_samples_leaf: {}'.format(search.best_estimator_.min_samples_leaf))
        print('min_samples_split: {}'.format(search.best_estimator_.min_samples_split))
        print('max_depth: {}\n'.format(search.best_estimator_.max_depth))

        print(search.best_score_)
    
    return search


def save_results(dtc):
    
    df = pd.read_csv("links.tsv", sep='\t')
    
    link_portal = df['Portal da Transparência']
    
    df, result_search = prepare_dataset(df, train=False)
    
    X = df.iloc[:, 2:].values
    y = df.iloc[:, 1:2].values
    
    y_pred = predict(dtc, X, y, verbose=False)
    
    df['Portal da Transparência'] = link_portal
    df['find_html'] = result_search
    df['predict'] = y_pred
    
    df.to_csv("predict.csv", index=False)


def main_dtc(verbose=True):
    
    df = pd.read_csv("links.tsv", sep='\t')
    df, _ = prepare_dataset(df, train=True)
    
    X = df.iloc[:, 2:].values
    y = df.iloc[:, 1:2].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    rus = RandomUnderSampler()
    X_train, y_train = rus.fit_resample(X_train, y_train)
    
    model = DecisionTreeClassifier()

    parameters = {'criterion': ('gini', 'entropy'),
              'splitter': ('best', 'random'),
              'min_samples_leaf':[5 , 8, 10, 13, 15, 18],
              'min_samples_split':[5, 10, 15, 20],
              'max_depth':[5, 10, 15]}

    #gsearch = test_parameters(X_train, y_train, model, parameters, search_model='gsearch')
    rsearch = test_parameters(X_train, y_train, model, parameters, search_model='rsearch')

    dtc = fit_dtc(
        X_train, y_train, criterion=rsearch.best_estimator_.criterion,
        splitter=rsearch.best_estimator_.splitter, min_samples_leaf=10,
        min_samples_split=rsearch.best_estimator_.min_samples_split,
        max_depth=rsearch.best_estimator_.max_depth)
    
    y_pred = predict(dtc, X_test, y_test)
    
    feature_names=['câmara', 'legislativo', 'controladoria-geral', 'plurianual', 'despesas',
                   'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                   'convênios', 'viagens', 'concurso', 'contas públicas', 'obras públicas',
                   'portal da transparência', 'transparência']
    
    plot_dtc(dtc, feature_names)

    save_results(dtc)


main_dtc()
