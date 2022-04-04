#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv(r'./dataset.csv')


# In[2]:


df.head()


# In[3]:


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
stop_words=set(stopwords.words('english'))
port=WordNetLemmatizer()


# In[4]:


def preprocess(text):
    def tokenization(simText):
        return word_tokenize(simText)
    def removeStopwords(token):
        return [w for w in token if not w in stop_words]
    def stemming(removeStopWords):
        return [port.lemmatize(word) for word in removeStopWords]
    return ' '.join(stemming(removeStopwords(tokenization(re.sub(r'[^\w\s]', '', text.lower())))))

df['filter email'] = df['email'].apply(preprocess)


# In[5]:


from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
cv = CountVectorizer()
tfidf = TfidfVectorizer(max_features=3000)

#turn frequency inverse docu fre
# In[6]:


X = tfidf.fit_transform(df['filter email']).toarray()


# In[7]:


from sklearn.model_selection import train_test_split


# In[8]:


X_train,X_test,y_train,y_test = train_test_split(X,df.label,test_size=0.3, random_state=42)




# In[16]:


from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)


svm = clf.predict(X_test)


# In[45]:


def get_result(text):
    pre_text = preprocess(text)
    vector_text = tfidf.transform([pre_text]).toarray()
    pred = clf.predict(vector_text)[0]
    if pred == 0:
        return 'This is not spam'
    else:
        return "This is spam"


# In[ ]:




