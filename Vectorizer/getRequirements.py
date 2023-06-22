#! /usr/bin/python3
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vec = CountVectorizer(strip_accents='unicode')
# connect to a database
connection = sqlite3.connect(os.path.realpath('../analyst.db'))
# create a "cursor" for working with the database
cursorRead = connection.cursor()
cursorWrite = connection.cursor()

cursorRead.execute("SELECT description FROM jobs;")
similarWords =    {'sql':['sql','mysql','postgresql'], 'python':['python','python3'],
                    'aws':['azure','aws'],
                   }
requirementTools = {'sql':0, 'python':0,'tableau':0,
                   'rstudio':0,'java':0,'aws':0,
                   'excel':0,'powerbi':0,'jupyter':0,
                   'pandas':0,'matplotlib':0,'seaborn':0,
                   }
requiredEducation = {'master': 0, 'bachelor':0}
requiredAtributes = {'visualize': 0, 'design': 0,
                    'develop': 0, 'clean': 0, 'assist': 0,
                    'predict': 0, 'code': 0, 'collect': 0,
                    'implement': 0, 'lead': 0,'expertise': 0,
                    'translate': 0, 'build': 0, 'report':0 
                    }
cursorWrite.execute("""CREATE TABLE IF NOT EXISTS requiredTools(
                               tool TEXT,
                               occurences INT);""")

cursorWrite.execute("""CREATE TABLE IF NOT EXISTS requiredAtributes(
                               atribute TEXT,
                               occurences INT);""")

normalizer = vec.build_analyzer()
normalizedText = []

for row in cursorRead:
    normalizedText.append(' '.join(normalizer(row[0])))
    
t= vec.fit_transform(normalizedText).toarray()

sumArr = np.sum(t,axis = 0)

for key in requirementTools.keys():
    if key in similarWords:
        for simWord in similarWords[key]:
            requirementTools[key] += sumArr[vec.vocabulary_[simWord]]
    else:
        requirementTools[key] = sumArr[vec.vocabulary_[key]]
    cursorWrite.execute("INSERT INTO requiredTools VALUES (?,?);""",(key,int(requirementTools[key])))

requiredEducation['master'] = sumArr[vec.vocabulary_['master']] + sumArr[vec.vocabulary_['masters']]  
requiredEducation['bachelor'] = sumArr[vec.vocabulary_['bachelor']] + sumArr[vec.vocabulary_['bachelors']]

for key in requiredAtributes.keys():
    requiredAtributes[key] += sumArr[vec.vocabulary_[key]]
    cursorWrite.execute("INSERT INTO requiredAtributes VALUES (?,?);""",(key,int(requiredAtributes[key])))
def showDesc(dict):
    for k,v in sorted(dict.items(), key = lambda x : x[1], reverse = True):
         print(k + " : " + str(v))
    print()

connection.commit()
connection.close()

print("requiredTools")
showDesc(requirementTools)
print("requiredEducation")
showDesc(requiredEducation)
print("requiredAtributes")
showDesc(requiredAtributes)

vectorizer2 = TfidfVectorizer(stop_words = 'english', max_features = 1000)
fittedText = vectorizer2.fit_transform(normalizedText)

fNames2 = vectorizer2.get_feature_names()

kmeans = KMeans(n_clusters = 3, n_init = 20)
kmeans.fit(fittedText)
common_words = kmeans.cluster_centers_.argsort()[:,-1:-50:-1]
for num, centroid in enumerate(common_words):
    print('cluster '+str(num) + ' : ' + ', '.join(fNames2[word] for word in centroid))
    print()
    
def frequencies_dict(cluster_index):
    term_frequencies = kmeans.cluster_centers_[cluster_index]
    sorted_terms = common_words[cluster_index]
    frequencies = {fNames2[i]: term_frequencies[i] for i in sorted_terms}
    return frequencies

for i in range(3):
    frequencies = frequencies_dict(i)
    wc = WordCloud(background_color= "white", max_words=50)
    wc.generate_from_frequencies(frequencies)
    fig, ax = plt.subplots()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    ax.set(title='Cluster ' + str(i))
    #fig.savefig("cluster" + str(i) + ".png")


