import statistics
import random

# OUTLINE 
# _______________________________________________
# Approach inspired by Bayesian probability is to have an initial belief about the 'true' rating
# of an item, and use user ratings to update this belief, meaning we will have to quantify an 
# initial rating for each item (using a 5 point scale, as most review systems do).
#
# As such, we require 2 parameters:
# - The 'true' default rating of an item, if there are no existing ratings
#   'R' -> the initial belief
#
# - The weight that we want to give this initial belief, versus subsequent ratings
#   'W' -> the weight of our initial belief, where belief 'R' is worth W user ratings 
# 
# EXAMPLE 
# _______________________________________________
# Assume you have W ratings of value R along with any user ratings, and find the average. 
# Given R=2 and W=3, where N is number of user ratings, V is their average
#
# Weighted_Rating = (R*W + N*V) / (W+N)
#
# 1. For 100 user ratings of 4 
# ∴ Weighted_Rating = (2*3 + 100*4) / (100 + 3) = 3.94☆
# In comparison, a straight average would give us a 4☆ rating.
#
# 2. For 3 ratings of 5 and 1 rating of 4
# ∴ Weighted_Rating = (2*3 + 3*5 + 4) / (3 + 4) = 3.57☆
# Average = 4.75☆
#
# 3. For 10 ratings of 4
# ∴ Weighted_Rating = (2*3 + 10*4) / (3 + 10) = 3.54☆
# Average = 4☆
#
# 4. For 1 ratings of 5
# ∴ Weighted_Rating = (2*3 + 5*1) / (3 + 1) = 2.75☆
# Average = 5☆
# 
# TODO Function to create better synthetic review data
# TODO Importation of actual review data from UberEats or Amazon :)
# TODO Find the related XKCD about how anything below 5 starts is shit
# TODO Transcribe rationale for this program from notes

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
    rating = ((r * w) + (g_mean * g_len)) / (w + g_len)
    return rating

list = ex5 # Select list

rating_avg = statistics.mean(list)
print("Mean: ", rating_avg)

rating = compute_rating(r, w, rating_avg, len(list))
print(rating)

# THOUGHTS 25/5/23
# Seems like it's more interesting to look at smaller numbers of reviews, as this
# is where we see significant differences in rating schemas. Over 1000 ratings we 
# can see that there is very little difference between the weighted rating, and 
# the mean rating.
#
# TODO Plot results to illustrate the above :)