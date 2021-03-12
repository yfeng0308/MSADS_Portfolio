#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import pandas as pd
import nltk
import re,os
import numpy as np
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
# read in dataframe
df=pd.read_csv('./nlp/Final_Project_Data.csv')
print(df.info())
df['text'] = df['text'].astype('str') 


# check and eliminate text that lenth less than 500
#delete_list=[]
#for index,text in zip(dataframe['text'].index,dataframe['text']):
#    if(len(text)<500):
#        delete_list.append(index)
#print('The number of text less than 500 is',len(delete_list))
#delete_df=dataframe.drop(delete_list)
#print(delete_df.info())

# sentence tokenization
sentences=[]
for text in df['text']:
    sentences.append(nltk.sent_tokenize(text))
sentences=[x for y in sentences for x in y] # flatten list
sentences[:10]

# remove punctuation, number and special characters
clean_sentences=pd.Series(sentences).str.replace("[^a-zA-Z]"," ")
clean_sentences[:10]

# make alphaabets lowercase
clean_sentences=[item.lower() for item in clean_sentences]
clean_sentences[:10]

# stop_words
stop_words = stopwords.words('english')
# function to remove stopwords
def remove_stopwords(sen):
  sen_new = " ".join([i for i in sen if i not in stop_words])
  return sen_new
# remove stopwords from sentences
clean_sentences=[remove_stopwords(item.split())for item in clean_sentences] 
clean_sentences[:10]

# download pretrained GloVe word embeddings
nltk.download('punkt')
import wget
Url="http://nlp.stanford.edu/data/glove.6B.zip"
filename=wget.download(Url)
import zipfile
zip=zipfile.ZipFile(filename)
zip.extractall()

# extract word vectors
word_embeddings={}
f=open('glove.6B.100d.txt',encoding='utf-8')
for line in f:
    values=line.split()
    words=values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[words]=coefs
f.close()

# sentences vectors
sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)

len(sentence_vectors)


##The next step is to find similarities among the sentences. 
##We will use cosine similarity to find similarity between a pair of sentences. 
##Let's create an empty similarity matrix for this task and populate it with cosine similarities of the sentences.

# similarity matrix
sim_mat = np.zeros([len(sentences),len(sentences)])
for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

# build ranked sentences


nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

# Specify number of sentences to form the summary
summary_n = 10

# Generate summary
for i in range(summary_n):
  print(ranked_sentences[i][1])
  
  
## define running function
def running_function_textrank(text):
    # prepare a list
    text_summary=[]
    # sentence tokenization
    sentences = nltk.sent_tokenize(text)
    if(len(sentences)==0):
        return text_summary
    # remove punctuation, number and special characters
    clean_sentences=pd.Series(sentences).str.replace("[^a-zA-Z]"," ")
    # make alphaabets lowercase
    clean_sentences=[item.lower() for item in clean_sentences]
    # remove stopwords from sentences
    clean_sentences=[remove_stopwords(item.split())for item in clean_sentences] 
    # sentences vectors
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
    # similarity matrix
    sim_mat = np.zeros([len(sentences),len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    # build ranked sentences
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank_numpy(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    sm=3
    if(len(ranked_sentences)<3):
        sm=len(ranked_sentences)
    # generate summary
    for i in range(sm):
        text_summary.append(ranked_sentences[i][1])
    return text_summary


# implement textrank to whose dataframe Time:
df['textrank_summarization']=df.text.apply(lambda x:running_function_textrank(x))

# test
empty_list=[]
count=0
for x in df['text']:
    empty_list.append(running_function_textrank(x))
    print(count)
    count+=1

summarization = []
for text in empty_list:
  sents=''
  for sent in text:
    sents += sent
  summarization.append(sents)

df['textrank_summarization'] = summarization

df.to_csv('./nlp/TextRank.csv',index=False)

textrank =pd.read_csv('./nlp/TextRank.csv')
textrank['textrank_summarization'][0]
textrank['text'][0]
df.info()

df=df.dropna()
df.info()
df[df['textrank_summarization']=='nan'].index[0]
df=df.drop(df[df['textrank_summarization']=='nan'].index[0])
df.info()
df[df['textrank_summarization']=='...'].index[0]
df=df.drop(df[df['textrank_summarization']=='...'].index[0])
df.to_csv('./nlp/TextRank_renew.csv',index=False)
df['textrank_summarization'][80261]
df['title'][80261]
df['textrank_summarization']
df['title'][666]
df['text'][666]
