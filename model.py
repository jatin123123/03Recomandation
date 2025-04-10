import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LinearRegression
from nltk.stem.porter import PorterStemmer

ps=PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

         

movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')
movies=movies.merge(credits,on='title')


movies=movies[['genres','movie_id','title','overview','keywords','cast','crew']]

movies.dropna(inplace=True)

import ast
def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

def cast(obj):
    l=[]
    cast_list=ast.literal_eval(obj)
    for i in cast_list[:3]:
        l.append(i['name'])
    return l
movies['cast']=movies['cast'].apply(cast)

def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name'])
    return l

movies['crew']=movies['crew'].apply(fetch_director)
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])


movies['tags']=movies['cast']+movies['crew']+movies['genres']+movies['keywords']+movies['overview']

new_df=movies[['movie_id','title','tags']]

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

new_df['tags']=new_df['tags'].apply(stem)
from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(max_features=5000,stop_words='english')

vector=cv.fit_transform(new_df['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vector)


# main Function

def recommend(movie):
    movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    for i in movie_list:
        print(new_df.iloc[i[0]]['title'])

    
    
recommend("Avatar")

import pickle 
pickle.dump(new_df,open('movies.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))