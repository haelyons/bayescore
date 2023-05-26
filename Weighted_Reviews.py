import statistics
import random
import tkinter as tk

# RELATED XKCD
# https://www.explainxkcd.com/wiki/index.php/1098:_Star_Ratings

# TODO Basic GUI for modifying R and W interactively as a way to understand
# their effects on the weighted rating - use matplotlib
# TODO Importation of actual review data from UberEats or Amazon :)
# TODO Plot results for shorter vs. longer datasets and similarity with mean

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

def update_rating():
    list = ex1  # Select list

    rating_avg = statistics.mean(list)
    rating = compute_rating(r, w, rating_avg, len(list))
    rating_label.config(text=f"Rating: {rating}")

def on_r_changed(event):
    new_r = int(r_entry.get())
    global r 
    r = new_r
    update_rating()

def on_w_changed(event):
    new_w = int(w_entry.get())
    global w
    w = new_w
    update_rating()

root = tk.Tk()
root.title("Rating Calculator")

r_label = tk.Label(root, text="R:")
r_label.grid(row=0, column=0, padx=5, pady=5)

r_entry = tk.Entry(root, width=5)
r_entry.insert(tk.END, str(r))
r_entry.grid(row=0, column=1, padx=5, pady=5)
r_entry.bind("<Return>", on_r_changed)

w_label = tk.Label(root, text="W:")
w_label.grid(row=1, column=0, padx=5, pady=5)

w_entry = tk.Entry(root, width=5)
w_entry.insert(tk.END, str(w))
w_entry.grid(row=1, column=1, padx=5, pady=5)
w_entry.bind("<Return>", on_w_changed)

rating_label = tk.Label(root, text="Rating: ")
rating_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

update_rating()

root.mainloop()