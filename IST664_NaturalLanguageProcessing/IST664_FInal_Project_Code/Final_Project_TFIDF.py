#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import pandas as pd
from nltk import sent_tokenize,word_tokenize,PorterStemmer
from nltk.corpus import stopwords
import re,os
import numpy as np
import math


# read in dataframe
dataframe=pd.read_csv('./nlp/Final_Project_Data.csv')
print(dataframe.info())
dataframe['text'] = dataframe['text'].astype('str')


# create frequency matrix of the words in each sentence  Time: 30mins
def create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix

# Calculate Term Frequency and generate a matrix   Time: 5s
def create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix

# create a table for documents per word
def create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table

# calculate IDF and generate a matrix
def create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

# calculate TF-IDF and generate a matrix
def create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix

# score the sentences
def score_sentences(tf_idf_matrix):
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """
    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        if(count_words_in_sentence==0):
            continue
        for word, score in f_table.items():
            total_score_per_sentence += score
            
        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue

# Find the threhold
def find_average_score(sentence_scores):
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentence_scores:
        sumValues += sentence_scores[entry]
    if(len(sentence_scores)==0):
        return 0
    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentence_scores))

    return average

# generate summary
def generate_summary(sentences, sentence_scores, average_score):
    summary =[]

    for sentence in sentences:
        if sentence[:15] in sentence_scores and sentence_scores[sentence[:15]] >= (average_score):
            summary.append(sentence)

    return summary


# define running function 
def running_function(text):
    sentences = sent_tokenize(text)
    frequency_matrix=create_frequency_matrix(sentences)
    tf_matrix=create_tf_matrix(frequency_matrix)
    count_doc_per_words=create_documents_per_words(frequency_matrix)
    total_documents=len(sentences)
    idf_matrix=create_idf_matrix(frequency_matrix, count_doc_per_words, total_documents)
    tf_idf_matrix=create_tf_idf_matrix(tf_matrix,idf_matrix)
    sentence_scores=score_sentences(tf_idf_matrix)
    average_score=find_average_score(sentence_scores)
    sentence_summary=generate_summary(sentences, sentence_scores, average_score)
    return sentence_summary

# implement TF-IDF to whole dataframe Time: 40mins
dataframe['summarization']=dataframe.text.apply(lambda x : running_function(x))

sum_list = dataframe['summarization']

summarization = []
for text in sum_list:
  sents=''
  for sent in text:
    sents += sent
  summarization.append(sents)

dataframe['summarization'] = sum_list

dataframe.to_csv('./nlp/TFIDF.csv',index=False)


tfidf=pd.read_csv('./nlp/TFIDF.csv')

tfidf[tfidf.isna()==True].index[0]

tfidf[tfidf['summarization']=='nan'].index[0]

tfidf['summarization'][42613]

pre = tfidf[['title','text']]
