


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
# ∴ Weighted_Rating = (2*3 + 5) / (3 + 1) = 2.75☆
# Average = 5☆
# 
# TODO Generalise looping over subsets to allow examples with multiple values
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
test = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]

def split_by_recurring_numbers(data):
    occurrences = {}
    result = []
    
    for num in data:
        if num in occurrences:
            occurrences[num] += 1
        else:
            occurrences[num] = 1
    
    temp_arr = []
    current_num = data[0]
    
    for num in data:
        if num == current_num:
            temp_arr.append(num)
        else:
            result.append(temp_arr)
            temp_arr = [num]
            current_num = num
    
    result.append(temp_arr)
    
    return result

def weighted_rating(r, w, data):
    recurrences = split_by_recurring_numbers(data)

    for group in recurrences:
        print("Group:", group)
        groupLength = len(group)
        for value in group:
            print("Value:", value)
            groupValue = value * groupLength
            print(groupValue)

    rating = ((r * w) + (groupValue)) / (w + len(data))
    return rating

computedRating = weighted_rating(r, w, test)
print(computedRating)