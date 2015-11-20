# AppEngine Movie Recommendation
A small movie recommendation web app in python

## About the app:

---version 1---

- The recommendation are based on item-based filtering.
- The recommendation code is in python. 
- It uses the ml-1m dataset(MovieLens 1 million ratings) for all its data(list of movies, users, ratings).
- The similarity matrix(euclid distance) for all item(3700 movies) is pre-calculated. It takes around 10 mins to compute this matrix
- The app asks you to give recommendations for 10 random movies. You submit your rating. 
- The algorithm then takes your movies, finds top matches from the similarity matrix and predicts your rating for a movie.
- These predictions along with their movie titles are displayed in decreasing order(unless a key error occurs)
- Being a open dataset, developed over time by different users, there are some missing/repeated values which might lead to key-errors. 

Refresh the page if you see a server error.

The application is written using webapp2 and is hosted on google app engine

<a href="http://priyam-mrec-1001.appspot.com/">Link to application</a>
