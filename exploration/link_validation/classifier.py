#!/usr/bin/env python
# coding: utf-8

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
import matplotlib.pyplot as plt


def cross_validation(model, X_train, y_train):
    
    kfold = model_selection.KFold(n_splits=10)
    results = model_selection.cross_val_score(model, X_train, y_train.ravel(), cv=kfold)
    print("Accuracy: %.3f%% (%.3f%%)" % (results.mean()*100.0, results.std()*100.0))

def plot_dtc(classifier, feature_names):
    
    fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
    plot_tree(classifier,
            filled = True,
            feature_names=feature_names);
    fig.savefig('imagename.png')

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

