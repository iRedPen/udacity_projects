
# coding: utf-8

# In[1]:

import sys
import pickle
sys.path.append("../tools/")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
from sklearn.cross_validation import train_test_split

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.svm import SVC
from sklearn import tree
from sklearn.grid_search import GridSearchCV
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score


# In[2]:

### Task 1: Select what features to use.
### I`ll start by having all the features

features_list = ['poi','salary',  'deferral_payments', 'total_payments', 'loan_advances', 
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 
                 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 
                 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

financial_features = ['salary', 'bonus','long_term_incentive','deferred_income','deferral_payments',   
                     'loan_advances','other', 'expenses', 'director_fees','total_payments',
                     'exercised_stock_options','restricted_stock','restricted_stock_deferred', 'total_stock_value']

email_features = ['to_messages', 'from_poi_to_this_person', 
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi'] 
### I excluded email_address because it's a text string


# In[3]:

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

df = pd.DataFrame.from_dict(data_dict, orient = 'index')
df.shape


# There are 146 rows in the data set and 21 rows

# In[4]:

df.head()


# In[5]:

### count how many POIs in the dataset
df["poi"].sum()


# In[6]:

df.info()


# In[7]:

# NaN are considered strings. They need to be replaced to null values
df.replace('NaN', np.nan, inplace = True)
df.info()


# In[8]:

### all columns has missing data except POI, I'll check if any row has missing data in all columns
df[df.loc[:, df.columns != 'poi'].isnull().all(axis=1)] 


# In[9]:

### dropping the row that missing all values 
df = df.drop(['LOCKHART EUGENE E'])


# In[10]:

df.describe()


# Based on the reviewing the enron61702insiderpay.pdf file, which the source of the financial features, I'll assume that any missing financial data is zero.

# In[11]:

df[financial_features] = df[financial_features].fillna(value=0)


# In[12]:

df.info()


# For the email features (except for email_address), each is missing the data for 60 rows. Let's check if they are for the same people.

# In[13]:

null_email_data = df['to_messages'].isnull()
df.loc[null_email_data == True]


# In[14]:

### I noticed that there is one record named "THE TRAVEL AGENCY IN THE PARK", so I'll drop it because it's not a person
df = df.drop(['THE TRAVEL AGENCY IN THE PARK'])


# The features are missing for the same people, and it is a mix between poi/non-poi.
# Let's check if the median for these features is different based on being poi.

# In[15]:

df.groupby('poi')[email_features].median()


# Instead of replacing the missing values blindly, I would replace with the median for the same group (poi/non-poi).

# In[16]:

for i in email_features:
    df[i] = df.groupby('poi')[i].apply(lambda x: x.fillna(x.median()))
df.head()


# In[17]:

### Task 2: Remove outliers 
### Let's visually assess the relationship between the financial features through a scatter matrix 
### For better visualization, I'll separate the payments from the stock values
from pandas.plotting import scatter_matrix
scatter_matrix(df[financial_features[:10]],figsize=(40, 40))
plt.show()


# In[18]:

scatter_matrix(df[financial_features[10:]],figsize=(40, 40))
plt.show()


# In[19]:

### Scatter Matrix for Email Features 
scatter_matrix(df[email_features],figsize=(15, 15))
plt.show()


# In[20]:

### It seems there is an outlier across most of the fininicial data. Let`s check what is it.
for i in financial_features:
    print 'Maximum value in', i, 'is', df[i].argmax(), 'with a value of', df[i].max()


# This outlier is for the sum of all the financial values from the PDF file so it needs to be dropped.

# In[21]:

df = df.drop(['TOTAL'])
### Let's check again the scatter plot
scatter_matrix(df[financial_features[:10]],figsize=(40, 40))
plt.show()


# Due to the limited size of the dataset, I don't think I need to try further to detect any outliers and maybe needed to detect POIs.

# In[22]:

df[(df[financial_features[:9]].sum(axis='columns') == df[financial_features[9]]) == False]


# In[23]:

df[(df[financial_features[10:13]].sum(axis='columns') == df[financial_features[13]]) == False]


# In[24]:

### Using the .loc indexer, I'll select the columns that needs to be updated with the finincial data as per the original PDF file
df.loc[['BELFER ROBERT'], financial_features] = [0, 0, 0, -102500, 0, 0, 0, 3285, 102500, 3285, 0, 44093, -44093, 0]
df.loc[['BHATNAGAR SANJAY'], financial_features] = [0, 0, 0, 0, 0, 0, 0, 137864, 0, 137864, 15456290, 2604490, -2604490, 15456290]


# In[25]:

df[(df[financial_features[:9]].sum(axis='columns') == df[financial_features[9]]) == False]


# In[26]:

df[(df[financial_features[10:13]].sum(axis='columns') == df[financial_features[13]]) == False]


# In[27]:

### Task 3: Create new feature(s)
### I`ll add four new features

### Before adding the features, I'll keep a copy of the original df and features list, to be compared later 
original_df = df
original_features = features_list

### Feature 1: ratio of emails from poi to the person out of the total number of recived emails
df['from_poi_ratio'] = df['from_poi_to_this_person'] / df['to_messages']

### Feature 2: ratio of emails to poi from the person out of the total number of semt emails
df['to_poi_ratio'] = df['from_this_person_to_poi'] / df['from_messages']

### Feature 3: ratio of bonus to the salary
df['bonus_to_salary_ratio'] = df['bonus'] / df['salary']

### Feature 4: total payments and stock vales
df['total_money'] = df['total_payments'] + df['total_stock_value']

features_list.append('from_poi_ratio')
features_list.append('to_poi_ratio')
features_list.append('bonus_to_salary_ratio')
features_list.append('total_money')

### Checking that the new features didn`t introduce NaN values (when denominator is zero)
df.isnull().sum()


# In[28]:

### let`s fill the NaN values with 0
df['bonus_to_salary_ratio'] = df['bonus_to_salary_ratio'].fillna(value=0)


# In[29]:

### Now let`s change the dataframe to a dictionary 
my_dataset = df.to_dict('index')


# In[30]:

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Will do the same for the dataset without the new features
original_dataset = original_df.to_dict('index')
original_data = featureFormat(original_dataset, original_features, sort_keys = True)
original_labels, original_features = targetFeatureSplit(original_data)


# In[31]:

### Task 4: Try a varity of classifiers

scaler = MinMaxScaler()
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.4, random_state=42)

### Create a pipeline to select the best classifier and 
### use use cross_val_score to see the f1 score based on the training data
classifiers = [DecisionTreeClassifier(), SVC(), KNeighborsClassifier(), RandomForestClassifier(), LogisticRegression()]
for classifier in classifiers:
    pipe = Pipeline([
        ('scaler', scaler),
        ('select_features', SelectKBest()),
        ('classifier', classifier)
        ])
    pipe.fit(features_train, labels_train)
    pred = pipe.predict(features_test)
    print classifier, f1_score(labels_test, pred)


# In[32]:

### Doing the same for the data without the new added features
original_features_train, original_features_test, original_labels_train, original_labels_test = train_test_split(original_features, original_labels, test_size=0.4, random_state=42)
classifiers = [DecisionTreeClassifier(), SVC(), KNeighborsClassifier(), RandomForestClassifier(), LogisticRegression()]
for classifier in classifiers:
    pipe = Pipeline([
        ('scaler', scaler),
        ('select_features', SelectKBest()),
        ('classifier', classifier)
        ])
    pipe.fit(original_features_train, original_labels_train)
    pred = pipe.predict(original_features_test)
    print classifier, f1_score(original_labels_test, pred)


# From the previous steps, the Decision Tree Classifier with the newly added features has the highest F1 Score. I'll use it forward to be tuned to try and achive a better score.

# In[33]:

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### will start by having the pipeline specificly for the DecisionTreeClassifier

pipe = Pipeline([
        ('scaler', scaler),
        ('select_features', SelectKBest()),
        ('dt', DecisionTreeClassifier())
        ])

### two parameters will be focused on. max_depth which is the maximum depth of the tree and 
### min_samples_split which is the minimum number of samples required to split an internal node
param_grid = {
    'select_features__k':[7,8,9,10,11,12,13,14,15],
    'dt__max_depth':[1,2,3,4,5,6,7,8,9,10],
    'dt__min_samples_split':[2,3,4,5,6,7,8,9,10]
    }

### do gridsearch to select the best values for both parameters 
search = GridSearchCV(pipe, param_grid, scoring='f1')
search.fit(features_train, labels_train)
print(search.best_params_)


# In[34]:

### Based on previous search, will assign the parameters that were tuned
best_k = search.best_params_['select_features__k']
best_min_samples_split = search.best_params_['dt__min_samples_split']
best_max_depth = search.best_params_['dt__max_depth']

### Freezing the pipeline based on the choosen parameters from the search
clf = Pipeline([
        ('scaler', scaler),
        ('select_features', SelectKBest(k=best_k)),
        ('dt', DecisionTreeClassifier(min_samples_split=best_min_samples_split, max_depth=best_max_depth))
        ])

### identifing the K_best features
search_best = search.best_estimator_.named_steps['select_features'] # locate SelectKBest in GridsearchCV
integer_index = search_best.get_support() # get a mask or an integer index of the features selected
selected_features = [] # The list of K best features
for bool, feature in zip(integer_index, features_list[1:]): #go through features list, excluding poi
    if bool:
        selected_features.append(feature) # append selected features
print selected_features


# In[35]:

### applying the test_classifier function to obtain the validate the precision and recall values
test_classifier(clf, my_dataset, features_list, 1000)


# Both precision and recall are above .5, which meets the set criteria

# In[36]:

### Task 6: Dumping classifier, dataset, and features_list 

dump_classifier_and_data(clf, my_dataset, features_list)

