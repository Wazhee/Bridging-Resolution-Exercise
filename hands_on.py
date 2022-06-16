#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Excercise I: Calculates the precision, recall, and f-score of the prediction made by the Machine(ISNOTES dataset)

# Python program to convert 
# ISNOTES JSON file to CSV 

import csv 
import json
import requests

file_name = "original1.json"
file_2 = "isnotes.bridging.jsonlines"

rst = []
rst2 = []

with open(file_2) as f:
    for line in f.readlines():
           rst.append(json.loads(line))
with open(file_name) as f:
    for line in f.readlines():
           rst2.append(json.loads(line))


# In[4]:


# collect predictions 
f = open(file_2)
f2 = open(file_name)

str1 = f.readline()
str2 = f2.readline()


# In[5]:


# collect every dictionary from bridging json file
data = dict()
diction_list = []


# convert json file to list of dictionary 
with open(file_2) as f:
    for line in f.readlines():
        data = json.loads(line)
        diction_list.append(data)


# In[6]:


# collect every dictionary from original1 json file 
data = dict()
orig_diction_list = []

with open(file_name) as f: 
    for line in f.readlines():
        data = json.loads(line)
        orig_diction_list.append(data)


# In[7]:


# function for evaluating predicted bridging 
# and actual bridging pairs 

def antecedents_precision(document1, document2, clusters):
    # initiallize 
    num_correct_antecedents = 0
    bridges = document1["bridging_pairs"]
    predictions = document2["pred_bridging_pairs"]
    

    for predict in predictions:
        for bridge in bridges:
    # check if anaphors match
           
            if(bridge[0] == [predict[0], predict[1]]):
    
    # check if gold antecedent is in predicted anatecedent 
               
                if(bridge[1] == [predict[2], predict[3]]):
                     num_correct_antecedents += 1
                
                else:
                    for cluster in clusters:
                        if([predict[2], predict[3]] in cluster and bridge[1] in cluster):
                            num_correct_antecedents += 1 
    # return the number of correctly predict anaphors
    return num_correct_antecedents


# In[8]:


# get number of predictions for specific document
def get_num_predictions(prediction_document):
    count = 0
    for predict in prediction_document["pred_bridging_pairs"]:
        count += 1
    return count


# In[9]:


# function for evaluating predicted bridging 
# and actual bridging pairs 
def anaphors_precision(document1, document2):
    num_correct_anaphors = 0
    bridges = document1["bridging_pairs"]
    predictions = document2["pred_bridging_pairs"]
    for bridge in bridges:
        for predict in predictions:
            # check if anaphors match
            if(bridge[0] == [predict[0], predict[1]]):
                num_correct_anaphors += 1 
    return num_correct_anaphors


# In[10]:


def get_pairs(bdoc, pdoc):
    count = 0
    bridges = bdoc["bridging_pairs"]
    predictions = pdoc["pred_bridging_pairs"]
    for bridge in bridges:
        count += 1
        
    return count


# In[11]:


# while looping through the bridging pair document
# the program loops through the prediction bridging pair document 
# the program finds the matching document in each dictionary list(diction_list & orig_diction_list)
num_correct_anaphors = 0
num_correct_antecedents = 0
total_predictions = 0
total_pairs = 0
for bridge_document in diction_list:
    document_name = bridge_document["doc_key"]
    for prediction_document in orig_diction_list:
        if(document_name == prediction_document["doc_key"]):
            num_correct_anaphors += anaphors_precision(bridge_document, prediction_document)
            num_correct_antecedents += antecedents_precision(bridge_document, prediction_document, bridge_document["clusters"])
            total_pairs += get_pairs(bridge_document, prediction_document)
            total_predictions += get_num_predictions(prediction_document)

# calculating anaphor precision, recall, and F1 scores
recall = (num_correct_anaphors / total_pairs) * 100
precision = (num_correct_anaphors / total_predictions) * 100
f1_anaphors = 2 * ((recall * precision) / (recall + precision))

# calculating antecedents precision, recall, and F1 scores
recall_anteced = (num_correct_antecedents / total_pairs) * 100
precision_anteced = (num_correct_antecedents / total_predictions) * 100
f1_anteced = 2 * ((recall_anteced * precision_anteced) / (recall_anteced + precision_anteced))


# In[12]:


# exercise 1.1 and 1.2 results 

print("Anaphor precision: ", precision, "%")
print("Anaphor Recall: ", recall, "%")
print("Anaphor F1 Score: ", f1_anaphors, "%")
print("*****************************************")
print("*****************************************")
print("Antecedent precision: ", precision_anteced, "%")
print("Antecedent recall: ", recall_anteced, "%")
print("Antecedent F1 Score: ", f1_anteced, "%")


# In[13]:


# Exercise Part II: Calculates the precision, recall, and f-score of the prediction made 
#                   by the Machine - predicted antecedents = gold antecendent && 
#                   predicted antecedents is coreferent with gold antecendent

import sklearn


# In[14]:


# converting the json files into dictionaries


# In[23]:


# collect one prediction
f = open(file_2)
f2 = open(file_name)

# collect every dictionary from bridging json file
data = dict()
bdocuments = []


# convert json file to list of dictionary 
with open(file_2) as f:
    for line in f.readlines():
        data = json.loads(line)
        bdocuments.append(data)


# In[24]:


# collect every dictionary from original1 json file 
data = dict()
pdocuments = []

with open(file_name) as f: 
    for line in f.readlines():
        data = json.loads(line)
        pdocuments.append(data)

# confirm they are all dictionaries


# In[56]:


# Flattening clusters
cluster = bdocuments[0]["clusters"]
bpairs = bdocuments[0]["bridging_pairs"]
# generated candidate antecedents 
ca_list = []

flat_cluster = []

for c in cluster:
    flat_cluster += c
    


# In[89]:


one_mention = [88, 88]
sentences = bdocuments[0]["sentences"]
word_count = 0
sent_count = 0

sentence = sentences[0]
for word in sentence:
    if(word_count == one_mention[0]):
        print("gold mention ", word_count, " belongs to sentence: ", sent_count)
    else:
        word_count += 1

ca_dict = dict()


# In[104]:


# get candidates before anaphor
count = 0
for pair in bpairs:
    anaphor = pair[0]
    
    # locate anaphor in the clusters
    cluster_pos = get_cluster_index(anaphor, flat_cluster)
    
    
    sent_pos = get_sentence(anaphor, sentences)
    
    # current mention sentecne position
    cm_sentence_pos = get_sentence(flat_cluster[cluster_pos], sentences)
    
    while(sent_pos -  current_mention_sentence <= 2 and cluster_pos >= 0):
        current_mention = flat_cluster[cluster_pos]
        if(flat_cluster[cluster_pos] != anaphor):
            ca_list.append(current_mention) 
        cluster_pos -= 1  # go to the previous mention
        
    ca_dict[count] = ca_list
    print(ca_list, "\n\n\n")
    ca_list = []
    count += 1


# In[101]:


ca_dict[2]


# In[73]:


# get candidates after anaphor


# In[54]:


def get_cluster_index(anaphor, clusters):
    count = 0
    for cluster in clusters:
        if anaphor == cluster:
            return count
        else:
            count += 1
    return -1


# In[48]:


# function for checking sentence number
def get_sentence(mention, sentences):
    word_count = 0
    sentence_count = 0
    for sentence in sentences:
        for word in sentence:
            if(word_count == mention[0]):
                return sentence_count
            else: 
                word_count += 1
        sentence_count += 1
    return -1


# In[49]:


print("mention [101, 103] was found in sentence ", get_sentence([101, 103], sentences))


# In[ ]:




