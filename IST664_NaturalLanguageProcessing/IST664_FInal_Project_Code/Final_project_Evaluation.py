#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import package
import json
import csv
import pandas as pd
import nltk
import re,os
import numpy as np
from rouge import Rouge

# define evaluation function
def rouge(a,b):
    rouge = Rouge()
    rouge_fscore=[]
    try:
        rouge_score = rouge.get_scores(a,b, avg=True) # a和b里面包含多个句子的时候用

    except (ValueError,TypeError):
        rouge_fscore=[0,0,0]
        return rouge_fscore
    
    rl =rouge_score["rouge-l"]
    r1 =rouge_score["rouge-1"]
    r2 =rouge_score["rouge-2"]
    rouge_fscore.append(rl['f'])
    rouge_fscore.append(r1['f'])
    rouge_fscore.append(r2['f'])
    return rouge_fscore

# read in TFIDF model data
tfidf_df=pd.read_csv('./nlp/TFIDF.csv')
tfidf_df['summarization']=tfidf_df['summarization'].astype('str')
tfidf_df['title']=tfidf_df['title'].astype('str')
tfidf_df.info()

# evaluate TFIDF using rl['f'] in rouge
evaluation_fscore_rl=[]
evaluation_fscore_r1=[]
evaluation_fscore_r2=[]
for index,row in tfidf_df.iterrows():
    evaluation_fscore_rl.append(rouge(row['summarization'],row['title'])[0])
    evaluation_fscore_r1.append(rouge(row['summarization'],row['title'])[1])
    evaluation_fscore_r2.append(rouge(row['summarization'],row['title'])[2])
# mean evaluation_f for TFIDF
evaluation_fscore_rl=np.array(evaluation_fscore_rl)
evaluation_fscore_r1=np.array(evaluation_fscore_r1)
evaluation_fscore_r2=np.array(evaluation_fscore_r2)
np.mean(evaluation_fscore_rl)
np.mean(evaluation_fscore_r1)
np.mean(evaluation_fscore_r2)

# read in TextRank model data
tr_df=pd.read_csv('./nlp/TextRank_renew.csv')
tr_df['textrank_summarization']=tr_df['textrank_summarization'].astype('str')
tr_df['title']=tr_df['title'].astype('str')
tr_df.info()

tr_df['textrank_summarization'].isnull().values.any()
tr_df['title'].isnull().values.any()

# evaluate TextRank using rl['f'] in rouge
tr_evaluation_fscore_rl=[]
tr_evaluation_fscore_r1=[]
tr_evaluation_fscore_r2=[]
count=0
for index,row in tr_df.iterrows():
    tr_evaluation_fscore_rl.append(rouge(row['textrank_summarization'],row['title'])[0])
    tr_evaluation_fscore_r1.append(rouge(row['textrank_summarization'],row['title'])[1])
    tr_evaluation_fscore_r2.append(rouge(row['textrank_summarization'],row['title'])[2])
    if(count>=80261):
        print(count)
    count+=1

# mean evaluation_f for TextRank
tr_evaluation_fscore_rl=np.array(tr_evaluation_fscore_rl)
tr_evaluation_fscore_r1=np.array(tr_evaluation_fscore_r1)
tr_evaluation_fscore_r2=np.array(tr_evaluation_fscore_r2)
np.mean(tr_evaluation_fscore_rl)
np.mean(tr_evaluation_fscore_r1)
np.mean(tr_evaluation_fscore_r2)

#print('The average F-Measure score for TFIDF model is',np.mean(evaluation_f))

#print('The average F-Measure score for TextRank model is',np.mean(tr_evaluation_f))
