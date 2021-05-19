from numpy.core.fromnumeric import size
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from collections import Counter
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from numpy import mean
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

df = pd.read_csv("links.tsv", sep='\t')
df['Link Correto'] = df['Link Correto'].replace(['x'], 1)
df['Link Correto'].fillna(0, inplace=True)

df.loc[:, "consegui_html"] = None

df.loc[:, "plurianual"] = 0
df.loc[:, "despesas"] = 0
df.loc[:, "receitas"] = 0
df.loc[:, "servidores"] = 0
df.loc[:, "orçamentária"] = 0
df.loc[:, "licitações"] = 0
df.loc[:, "contratos"] = 0
df.loc[:, "inexigibilidade"] = 0
df.loc[:, "dispensa"] = 0
df.loc[:, "concurso"] = 0
df.loc[:, "contas públicas"] = 0
df.loc[:, "obras públicas"] = 0
df.loc[:, "portal da transparência"] = 0
df.loc[:, "transparência"] = 0
# df.loc[:, "link transparência"] = 0 ######

# df.loc[:, "portal no link"] = 0

targets_for_text = ['plurianual', 'despesas', 'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                    'dispensa', 'concurso', 'contas públicas', 'obras públicas', 'portal da transparência', 'transparência']
targets = '|'.join(targets_for_text)

def pontuar_texto(text):
    find = re.findall(targets, text)
    return (find)

def pontuar_os_municipios():

    count = 0
    for municipio in df.loc[:, 'Município']:
        name = 'portais/' + str(count) + '.html'
        try:
            with open(name, 'r') as arq:
                page = arq.read()
                text = BeautifulSoup(page, "html5lib").get_text().lower()
                if len(text) < 300:
                    df.loc[count, "consegui_html"] = 0
                else: 
                    df.loc[count, "consegui_html"] = 1

                portal_estadual = re.findall('portaltransparencia.gov.br', df.loc[count, 'Portal da Transparência'])
                if portal_estadual:
                    df.loc[count, "consegui_html"] = None

                # link_transp = re.findall('transparencia|tp|portal-da-transparencia|portal', df.loc[count, 'Portal da Transparência']) 
                # for palavra in link_transp:
                #     df.loc[count, "link transparência"] = +1
                
                # print(text)
                find_targets = pontuar_texto(text)
                for palavra in find_targets:
                    df.loc[count, palavra] += 1
            count += 1
        except:
            count += 1
            continue


def Decision_Tree_Classification( X_train, X_test, y_train, y_test):

    classifier = DecisionTreeClassifier(criterion = 'gini', random_state = 0, min_samples_leaf = 5)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    ac = accuracy_score(y_test, y_pred)

    print('Dec. Tree Class.: ', ac)

    fn=['consegui_html','plurianual','despesas','receitas','servidores','orçamentária','licitações','contratos',
        'inexigibilidade','dispensa','concurso','contas públicas','obras públicas','portal da transparência','transparência']
    fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
    plot_tree(classifier,
            filled = True,
            feature_names=fn,
            class_names=True);
    fig.savefig('imagename2.png')
    # data = df
    # data = data.dropna(subset=['consegui_html'])
    # data = data.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    # z_pred = classifier.predict(data.iloc[ :, 2:].values)
    # print (z_pred.tolist().count(1))

    return y_test, y_pred

def classificar(dataset):

    X = dataset.iloc[:, 2:]
    y = dataset.iloc[:, 1]

    # With ndersampling the model is getting worse 
    # under = RandomUnderSampler()
    # # fit and apply the transform
    # X, y = under.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.6, random_state = 1)

    # print('X_train',X_train.shape)
    # print('X_test',X_test.shape)
    # print('y_train',y_train.shape)
    # print('y_test',y_test.shape)

    y_test, y_pred = Decision_Tree_Classification(X_train, X_test, y_train, y_test)


def main():
    pontuar_os_municipios()
    dataset = df.loc[ : 301, :]

    dataset = dataset.dropna(subset=['consegui_html'])
    dataset = dataset.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    print(dataset.shape)

    dataset.to_csv("data.csv", index = False)
    classificar(dataset)

main()
