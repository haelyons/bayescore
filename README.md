# Outline 
Approach inspired by Bayesian probability is to have an initial belief about the 'true' rating
of an item, and use user ratings to update this belief, meaning we will have to quantify an 
initial rating for each item (using a 5 point scale, as most review systems do).

As such, we require 2 parameters:
- The 'true' default rating of an item, if there are no existing ratings
  'R' -> the initial belief

 - The weight that we want to give this initial belief, versus subsequent ratings
   'W' -> the weight of our initial belief, where belief 'R' is worth W user ratings 

# Examples 
Assume you have W ratings of value R along with any user ratings, and find the average. 
Given R=2 and W=3, where N is number of user ratings, V is their average

Weighted_Rating = (R*W + N*V) / (W+N)

1. For 100 user ratings of 4
∴ Weighted_Rating = (2*3 + 100*4) / (100 + 3) = 3.94☆
In comparison, a straight average would give us a 4☆ rating.

2. For 3 ratings of 5 and 1 rating of 4
∴ Weighted_Rating = (2*3 + 3*5 + 4) / (3 + 4) = 3.57☆
Average = 4.75☆

3. For 10 ratings of 4
∴ Weighted_Rating = (2*3 + 10*4) / (3 + 10) = 3.54☆
Average = 4☆

4. For 1 ratings of 5
∴ Weighted_Rating = (2*3 + 5*1) / (3 + 1) = 2.75☆
Average = 5☆
