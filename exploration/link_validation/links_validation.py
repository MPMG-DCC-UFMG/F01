# -*- coding: utf-8 -*-
# +
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import hyperparameter_optimization
import classifier
import preprocess
import create_occurrence_matrix 


# -

def save_results(dtc):
    
    df = pd.read_csv("links.tsv", sep='\t')
    
    link_portal = df['Portal da Transparência']
    
    df, result_search = create_occurrence_matrix .main(df, train=False)
    
    X = df.iloc[:, 2:].values
    y = df.iloc[:, 1:2].values
    
    y_pred = classifier.predict(dtc, X, y, verbose=False)
    
    df['Portal da Transparência'] = link_portal
    df['find_html'] = result_search
    df['predict'] = y_pred
    
    df.to_csv("predict.csv", index=False)


def main_dtc(verbose=True):
    
    df = pd.read_csv("links.tsv", sep='\t')
    df, _ = create_occurrence_matrix.main(df, train=True)
    
    X = df.iloc[:, 2:].values
    y = df.iloc[:, 1:2].values
    
    X = preprocess.tf_idf(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=43)

    X_train, y_train = preprocess.balance_data (X_train, y_train,random_state=42)

    parameters = {'criterion': ('gini', 'entropy'),
              'splitter': ('best', 'random'),
              'min_samples_leaf':[5 , 8, 10, 13, 15, 18],
              'min_samples_split':[5, 10, 15, 20],
              'max_depth':[5, 10, 15]}

    #gsearch = hyperparameter_optimization.test_parameters(
        #X_train, y_train, model, parameters, search_model='gsearch')
    rsearch = hyperparameter_optimization.test_parameters(
        X_train, y_train, DecisionTreeClassifier(), parameters, search_model='rsearch')

    dtc = classifier.fit_dtc(
        X_train, y_train, criterion=rsearch.best_estimator_.criterion,
        splitter=rsearch.best_estimator_.splitter,
        min_samples_leaf=rsearch.best_estimator_.min_samples_leaf,
        min_samples_split=rsearch.best_estimator_.min_samples_split,
        max_depth=rsearch.best_estimator_.max_depth)
    
    y_pred = classifier.predict(dtc, X_test, y_test)
    
    feature_names=['câmara', 'legislativo', 'controladoria-geral', 'plurianual', 'despesas',
                   'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                   'convênios', 'viagens', 'concurso', 'contas públicas', 'obras públicas',
                   'portal da transparência', 'transparência']
    
    classifier.plot_dtc(dtc, feature_names)

    save_results(dtc)


main_dtc()
