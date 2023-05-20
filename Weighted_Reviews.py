
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
# 1. For 100 user ratings of 4 [ (R*W + N*V) / (W+N)]
# ∴ (2*3 + 100*4) / (100 + 3) = 3.94☆
# In comparison, using normal averaging would give us a 4☆ rating.
#
# TODO Further examples (3 more written)
# TODO Actual implementation of the base function
# TODO Function to create synthetic review data
# TODO Importation of actual review data from UberEats or Amazon :)