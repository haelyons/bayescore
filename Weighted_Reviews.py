import statistics
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# RELATED XKCD
# https://www.explainxkcd.com/wiki/index.php/1098:_Star_Ratings

# TODO Basic GUI for modifying R and W interactively as a way to understand
# their effects on the weighted rating - use matplotlib
# TODO Importation of actual review data from UberEats or Amazon :)
# TODO Plot results for shorter vs. longer datasets and similarity with mean

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

def recursive_compute(r, w, g_mean, g_len, list):
    tempRating = 0
    currentRating = (currentRating + tempRating) / 2
    for rating in list:
        


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


# Create the figure and the line that we will manipulate
n = np.linspace(0,len(list), len(list))
fig, ax = plt.subplots()
line, = ax.plot(n, compute_rating(r, w, rating_avg, len(list)), lw=2)

# Adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

ax.set_xlabel('Reviews [n]')

# Make a horizontal slider to control the initial rating.
r_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
r_slider = Slider(
    ax=r_ax,
    label='Initial Rating',
    valmin=0,
    valmax=10,
    valinit=r,
)

# Make a vertically oriented slider to control the weight of the initial rating
w_ax = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
w_slider = Slider(
    ax=w_ax,
    label="Weight of Initial Rating",
    valmin=0,
    valmax=10,
    valinit=w,
    orientation="vertical"
)

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(compute_rating(r_slider, w_slider, rating_avg, len(list)))
    fig.canvas.draw_idle()

# register the update function with each slider
r_slider.on_changed(update)
w_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    r_slider.reset()
    w_slider.reset()
button.on_clicked(reset)

plt.show()