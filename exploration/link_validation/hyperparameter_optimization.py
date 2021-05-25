#!/usr/bin/env python
# coding: utf-8

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import model_selection

def grid_search(parameters, model, X_train, y_train):
    
    gsearch = GridSearchCV(model, parameters)
    gsearch.fit(X_train, y_train.ravel())
    
    return gsearch

def randomized_search (parameters, model, X_train, y_train):
    
    rsearch = RandomizedSearchCV(estimator=model, param_distributions=parameters, n_iter=100, random_state=42)
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

