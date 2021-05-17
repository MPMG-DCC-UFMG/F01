import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


# print(df.describe())

df = pd.read_csv("links.tsv", sep='\t')
df = df.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
df['Link Correto'] = df['Link Correto'].replace(['x'], 1)
df['Link Correto'].fillna(0, inplace=True)

df.loc[:, "consegui_html"] = None

# df.loc[:, "numero_de_tags"] = 0
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
df.loc[:, "portal no link"] = 0


targets_for_text = ['plurianual', 'despesas', 'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade', 'dispensa', 'concurso', 'contas públicas', 'obras públicas']
not_include = ['403 Forbidden']
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
                # print(text)
                palavras = pontuar_texto(text)
                find_targets =  set(palavras)
                for palavra in find_targets:
                    df.loc[count, palavra] = 1
            count += 1
        except:
            count += 1
            continue


def Naive_Bayes(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = GaussianNB()
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Naice_Bayes: ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 1:].values)
    # print (z_pred.tolist().count(0))

def Random_Florest(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Random_Florest: ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 1:].values)
    # print (z_pred.tolist().count(0))

def Kernel_SVM(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = SVC(kernel = 'rbf', random_state = 0)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Kernel_SVM: ', ac)

    data = df.dropna(subset=['consegui_html'])
    z_pred = classifier.predict(data.iloc[ :, 2:].values)
    print (z_pred.tolist().count(1))

def SVM(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = SVC(kernel = 'linear', random_state = 0)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Support Vector Machine(SVM): ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 1:].values)
    # print (z_pred.tolist().count(0))


def Logistic_Regression(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Logistic Regression: ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 1:].values)
    # print (z_pred.tolist().count(0))

def Decision_Tree_Classification(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('Dec. Tree Class.: ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 1:].values)
    # print (z_pred.tolist().count(0))

def K_NN(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7, random_state = 0)
    classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    ac = accuracy_score(y_test, y_pred)
    print('K-Nearest Neighbors (K-NN): ', ac)

    # z_pred = classifier.predict(df.iloc[ :, 2:].values)
    # print (z_pred.tolist().count(0))





def classificar(dataset):

    X = dataset.iloc[:, 2:].values
    y = dataset.iloc[:, 1:2].values
    dataset.to_csv("data.csv", index = False)

    # Feature Scaling    
    # sc = StandardScaler() 
    # X_train = sc.fit_transform(X_train)
    # X_test = sc.transform(X_test)

    # Random_Florest(X,y)
    # Naive_Bayes(X,y)
    Kernel_SVM(X,y)
    # SVM(X,y)
    # Logistic_Regression(X,y)
    # Decision_Tree_Classification(X,y)
    # K_NN(X,y)


def main():
    pontuar_os_municipios()
    dataset = df.loc[ :89, :]
    dataset = dataset.dropna(subset=['consegui_html'])
    # df = df.dropna(subset=['consegui_html'])
    classificar(dataset)

    # TESTAR ALGUM
    # with open('portais/839.html', 'r') as arq:
    #     page = arq.read()
    #     text = BeautifulSoup(page, "html5lib").get_text().lower()
    #     print(len(text))
    # print(df.iloc[ :89, :5])


main()
