#! /usr/bin/python3
import sqlite3
import os
import numpy as np

# connect to a database
connection = sqlite3.connect(os.path.realpath('../analyst.db'))
# create a "cursor" for working with the database
cursorRead = connection.cursor()


decForInformation  = cursorRead.execute("SELECT description FROM jobs WHERE sector = 'Information Technology';")

requirementToolsINF = {'sql':0, 'python':0,'tableau':0,
                   'java':0,'aws':0,
                   'excel':0,'powerbi':0,'jupyter':0,
                   'pandas':0,'matplotlib':0
                   }
requirementToolsFIN = {'sql':0, 'python':0,'tableau':0,
                   'java':0,'aws':0,
                   'excel':0,'powerbi':0,'jupyter':0,
                   'pandas':0
                   }

similarWords =    {'sql':['sql','postgresql'], 'python':['python'],
                    'aws':['azure','aws'],
                   }
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
vec = CountVectorizer(strip_accents='unicode')


normalizer = vec.build_analyzer()
normalizedTextForInformation = []
normalizedTextForFinance = []

for row in cursorRead:
    normalizedTextForInformation.append(' '.join(normalizer(row[0])))
cursorRead.execute("SELECT description FROM jobs WHERE sector = 'Finance';")

for row in cursorRead:
    normalizedTextForFinance.append(' '.join(normalizer(row[0])))

cursorWrite.execute("""CREATE TABLE IF NOT EXISTS requiredToolsFIN(                  
        tool TEXT, 
        occurences INT);""") 
cursorWrite.execute("""CREATE TABLE IF NOT EXISTS requiredToolsINF(    
                    atribute TEXT,  
                    occurences INT);""")    
tINF= vec.fit_transform(normalizedTextForInformation).toarray()
sumArr = np.sum(tINF,axis = 0)

for key in requirementToolsINF.keys():
    if key in similarWords:
        for simWord in similarWords[key]:
            requirementToolsINF[key] += sumArr[vec.vocabulary_[simWord]]
    else:
        requirementToolsINF[key] = sumArr[vec.vocabulary_[key]]
    cursorWrite.execute("INSERT INTO requiredToolsINF VALUES (?,?);""",(key,int(requirementToolsINF[key])))


tFIN= vec.fit_transform(normalizedTextForFinance).toarray()
sumArr = np.sum(tFIN,axis = 0)

for key in requirementToolsFIN.keys():
    if key in similarWords:
        for simWord in similarWords[key]:
            requirementToolsFIN[key] += sumArr[vec.vocabulary_[simWord]]
    else:
        requirementToolsFIN[key] = sumArr[vec.vocabulary_[key]]
    cursorWrite.execute("INSERT INTO requiredToolsFIN VALUES (?,?);""",(key,int(requirementToolsFIN[key])))
        
def showDesc(dict):
    for k,v in sorted(dict.items(), key = lambda x : x[1], reverse = True):
         print(k + " : " + str(v))
    print()

print("requiredToolsINF")
showDesc(requirementToolsINF)
print("requiredToolsFIN")
showDesc(requirementToolsFIN)

connection.close()
