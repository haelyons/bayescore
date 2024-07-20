import statistics
import random

# RELATED XKCD
# https://www.explainxkcd.com/wiki/index.php/1098:_Star_Ratings

# TODO 2 mode implementation 
# -- "Playground" for interactively modifying R and W using the example review sets below
# -- "Map" using the Google Maps API to generate new ratings for restaurants in a specific area

global r
global w

r = 2
w = 3

ex1 = [4] * 100
ex3 = [4] * 10
ex3 = [4] * 10
ex4 = [5] * 1
ex4b = [5] * 100
ex5 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]

def upperList():
    list = []
    for i in range(0,1000):
        if 400 < i < 600:
            list.append(4)
        else:
            list.append(5)
    return list

def randomList():
    list = []
    for i in range(0,1000):
        n = random.randint(0,5)
        list.append(n)
    return list

def compute_rating(r, w, g_mean, g_len):
    return ((r * w) + (g_mean * g_len)) / (w + g_len)

list = ex1 # Select list

rating_avg = statistics.mean(list)
print("Mean: ", rating_avg)

rating = compute_rating(r, w, rating_avg, len(list))
print(rating)

# THOUGHTS 25/5/23
# Seems like it's more interesting to look at smaller numbers of reviews, as this
# is where we see significant differences in rating schemas. Over 1000 ratings we 
# can see that there is very little difference between the weighted rating, and 
# the mean rating.
