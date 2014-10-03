# -*- coding: cp1252 -*-
import webapp2
import cgi
import pickle
import random
#import alg

def getRecMovies(userPref,itemPref):
    # find the user ratings items
    # find similar items from pref
    userRatings = userPref
    sum_sim={}
    total_sim={}

    # loop over items,rating rated by user
    for (item,rating) in userRatings.items():
        # loop over similar items to this item
        for (similarity,item2) in itemPref[item]:

            if item2 in userRatings:
                continue

            total_sim.setdefault(item2,0)
            total_sim[item2] += similarity*rating

            sum_sim.setdefault(item2,0)
            sum_sim[item2] += similarity

    rank = [((total_sim[item]/sum_sim[item]),item) for item in total_sim]
    rank.sort()
    rank.reverse()

    return rank[:75]

fo = open('movie_list','r')
movies = pickle.load(fo)
fo.close()
fo = open('genre_list','r')
genre_list = pickle.load(fo)
fo.close()
fo = open('euclidSim25','r')
itemPref = pickle.load(fo)
fo.close()

mainpage='''about the app:<br>...<br>...
            <br><p>
                    ---version 1---<br>
                    The recommendation are based on item-based filtering.<br>
                    The recommendation code is in python. <br>
                    It uses the ml-1m dataset for all its data(list of movies, users, ratings) <a href="http://grouplens.org/datasets/movielens/">movielens</a><br>
                    The similarity matrix for all item(3700 movies) is pre-calculated. It takes around 10 mins to compute this matrix<br>
                    The app asks you to give recommendations for 10 random movies. You submit your rating. <br>
                    The algorithm then takes your movies, finds top matches from the similarity matrix and predicts your rating for a movie.<br>
                    These predictions along with their movie titles are displayed in decreasing order(unless a key error occurs)<br>
                    Being a open dataset, developed over time by different users, there are some missing/repeated values which might lead to key-errors.
                    <br>
                    <br>
                    Refresh the page if you see a server error.<br>
                    The application is written using webapp2 and is hosted on google app engine</p><br>
            Click <form method="get" action="/getrec"><input type="submit" value="getrec"></form> to get
            recommendations.'''
refresh = '''
            <form method = "get">
                Refresh movie list<br>
                <input type ="submit">'''

form = '''
    <form method="post" action="/rec">
        %(error)s
        
        <div>Please enter a rating from 1(lowest) to 5(highest) for the given
        movies.<br>The movies have been picked randomly.<br>Enter 0 if
        you have not seen the movie<br>
        The form does not validate, so just don't.<br>
        <br>Refresh the page if you want another set of movies<br><br></div>

        <div>
        <lable>%(t1)s
        <input type = "text", name="r1" value="%(r1)s" required>
        </lable>
        <br>
            
        <lable>%(t2)s
        <input type = "text", name="r2" value="%(r2)s" required>
        </lable>
        <br>

        <lable>%(t3)s
        <input type = "text", name="r3" value="%(r3)s" required>
        </lable>
        <br>

        <lable>%(t4)s
        <input type = "text", name="r4" value="%(r4)s" required>
        </lable>
        <br>

        <lable>%(t5)s
        <input type = "text", name="r5" value="%(r5)s" required>
        </lable>
        <br>

        <lable>%(t6)s
        <input type = "text", name="r6" value="%(r6)s" required>
        </lable>
        <br>

        <lable>%(t7)s
        <input type = "text", name="r7" value="%(r7)s" required>
        </lable>
        <br>

        <lable>%(t8)s
        <input type = "text", name="r8" value="%(r8)s" required>
        </lable>
        <br>

        <lable>%(t9)s
        <input type = "text", name="r9" value="%(r9)s" required>
        </lable>
        <br>

        <lable>%(t10)s
        <input type = "text", name="r10" value="%(r10)s" required>
        </lable>
        <br>

        </div>
        <br>
        <br>
        <input type = "submit" value="submit"><br>
        
        <input type="hidden" name="t1" value="%(t1)s"><br>
        <input type="hidden" name="t2" value="%(t2)s"><br>
        <input type="hidden" name="t3" value="%(t3)s"><br>
        <input type="hidden" name="t4" value="%(t4)s"><br>
        <input type="hidden" name="t5" value="%(t5)s"><br>
        <input type="hidden" name="t6" value="%(t6)s"><br>
        <input type="hidden" name="t7" value="%(t7)s"><br>
        <input type="hidden" name="t8" value="%(t8)s"><br>
        <input type="hidden" name="t9" value="%(t9)s"><br>
        <input type="hidden" name="t10" value="%(t10)s"><br>
        
    </form>
        '''        
t={'t2': 'French Connection, The (1971)', 't3': 'Guys and Dolls (1955)', 't1': 'Live Flesh (1997)'}

def new_movies():
    movie_list = [movies[str(x)] for x in random.sample(xrange(1, 3884), 10)]
    index  =  dict((x+1,movie_list[x]) for x in range(0,10))
    dict_titles = dict(('t'+str(x),index[x]) for x in range(1,11))
    return dict_titles

def escape(s):
    return cgi.escape(s,quote=True)

def valid_input(x):
    if len(x)!=0:
        try:
            float(x)
            return True 
        except:
            return False
    else:
        return False

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(mainpage)

class RecHandler(webapp2.RequestHandler):
    def generate_new_form(self,dict_titles,user_ratings,errors):
        fill = {}
        for e in dict_titles:
            fill[e] = dict_titles[e]
        for e in user_ratings:
            fill[e] = user_ratings[e]
        for e in errors:
            fill[e] = errors[e]
        
        return form%fill
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        default_ratings = dict(('r'+str(x),'""') for x in range(1,11))
        global temp
        self.titles= new_movies()
        self.response.write(self.generate_new_form(self.titles,default_ratings,{'error':''}))
            
class ShowRec(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<br>...<br>nice try<br>Click <form method="get" action="/getrec"><input type="submit" value="getrec"></form> to get recommendations.')
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        check=True
        user_ratings=[self.request.get('r'+str(i)) for i in range(1,11)]
        temp = [self.request.get('t'+str(i)) for i in range(1,11)]
        
        #self.response.write('...its working<br><br>')
        userPref= {}
        for i in range(0,10):
            userPref[temp[i]] = float(user_ratings[i])

        #self.response.write(str(len(user_ratings))+","+str(len(temp))+","+str(len(itemPref))+","+str(len(userPref))+'<br>')
        recommendations = getRecMovies(userPref,itemPref)
        #self.response.write('...its working<br><br>')
        self.response.write('Top recommendations for you:<br><br>')
        for i in recommendations:
            self.response.write(i[1]+":"+str(i[0])+"<br>")
            

app = webapp2.WSGIApplication([
                                        ('/', MainPage),
                                        ('/getrec', RecHandler),
                                        ('/rec',ShowRec),
                                        ], debug=True)  

