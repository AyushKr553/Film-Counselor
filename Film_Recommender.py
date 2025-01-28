import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Correct file path
movies = pd.read_csv(r"C:\Users\KIIT01\Desktop\project\archive\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\KIIT01\Desktop\project\archive\tmdb_5000_credits.csv")

# Display the first 3 rows
print(movies.head(3))
print(credits.head(3))
print(movies.shape)
print(credits.shape)
movies=movies.merge(credits, on='title')
print(movies.head(3))
print(movies.iloc[0]['original_language'])
print(movies['original_language'].value_counts())
print(movies.columns)
print(movies[[]])
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
print(movies.head())
print(movies.shape)
print(movies.isnull().sum())
print(movies.dropna(inplace=True))
print(movies.isnull().sum())
print(movies.shape)
print(movies.duplicated().sum())
print(movies.iloc[0]['genres'])

import ast
def convert(text):
    l=[]
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l
print(movies['genres'].apply(convert))
movies['genres']=movies['genres'].apply(convert)
print(movies.head(3))

print(movies.iloc[0]['keywords'])
movies['keywords']=movies['keywords'].apply(convert)
print(movies.head(3))

print(movies.iloc[0]['cast'])
def convert_cast(text):
    l=[]
    counter=0
    for i in ast.literal_eval(text):
        if counter<6:
            l.append(i['name'])
        counter+=1
    return l
movies['cast']=movies['cast'].apply(convert_cast)
print(movies.head(3))

print(movies.iloc[0]['crew'])
movies['crew']=movies['crew'].apply(convert)
print(movies.head(2))

print(movies.iloc[0]['overview'])
movies['overview']=movies['overview'].apply(lambda x:x.split())
print(movies.head(2))

def remove_space(word):
    l=[]
    for i in word:
        l.append(i.replace(" ",""))
    return l
movies['cast']=movies['cast'].apply(remove_space)
movies['crew']=movies['crew'].apply(remove_space)
movies['genres']=movies['genres'].apply(remove_space)
movies['keywords']=movies['keywords'].apply(remove_space)
print(movies.head())

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
print(movies.head())
print(movies.iloc[0]['tags'])

new_df=movies[['movie_id','title','tags']]
print(new_df.head())

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
print(new_df.head())
print(new_df.iloc[0]['tags'])
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
print(new_df.sample) 
print(new_df.iloc[0]['tags'])

import nltk
from nltk.stem import PorterStemmer
ps=PorterStemmer()

def stems(text):
    l=[]
    for i in text.split():
        l.append(ps.stem(i))

    return " ".join(l)
new_df['tags']=new_df['tags'].apply(stems)
print(new_df.iloc[0]['tags'])

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
print(vector)
print(vector.shape)

from sklearn.metrics.pairwise import cosine_similarity
similary=cosine_similarity(vector)
print(similary)
print(similary.shape)

print(new_df[new_df['title']=='Spider-Man'].index[0])

def recommend(movie):
    index=new_df[new_df['title']==movie].index[0]
    distances=sorted(list(enumerate(similary[index])),reverse=True,key=lambda x:x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)
recommend('Spider-Man')
recommend('The Dark Knight Rises')

import pickle
pickle.dump(new_df, open('C:/Users/KIIT01/Desktop/project/artificats/movie_list.pkl', 'wb'))
pickle.dump(similary,open('C:/Users/KIIT01/Desktop/project/artificats/similarity.pkl','wb'))