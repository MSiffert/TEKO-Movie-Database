import tkinter as tk
from tkinter import Toplevel, Label, Button, PhotoImage
import sqlite3
from tkinter import messagebox
import requests

import movie
from movie import Movie


def open_login_window():
    login_window = tk.Toplevel(app)
    login_window.title("Login")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window, width=25)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=25, show='*')
    password_entry.pack(pady=5)

    button = tk.Button(login_window, text="Login",
                             command=lambda: login(username_entry.get(), password_entry.get(), login_window))
    button.pack(pady=10)

    login_window.grab_set()
    login_window.focus_set()
    login_window.wait_window()


def open_register_window():
    register_window = tk.Toplevel(app)
    register_window.title("Register")

    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window, width=25)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, width=25, show='*')
    password_entry.pack(pady=5)

    register_button = tk.Button(register_window, text="Register",
                             command=lambda: register(username_entry.get(), password_entry.get(), register_window))
    register_button.pack(pady=10)

    register_window.grab_set()
    register_window.focus_set()
    register_window.wait_window()


def login(username, password, window):
    url = "http://localhost:5142/users/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    json = response.json()

    if response.status_code == 200 and json.get('isSucceeded') is True:
        messagebox.showinfo("Login Successful", "You are now logged in!")
        global current_user_id
        current_user_id = json.get('userId')
        login_button.destroy()
        register_button.destroy()
        app.title("Movie Database: Username")
        window.destroy()

        if len(movie_list) > 0:
            show_movie_details(0)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials or server error!")


def register(username, password, window):
    url = "http://localhost:5142/users/register"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)

    if response.status_code == 200 and response.json().get('isSucceeded') is True:
        messagebox.showinfo("Register Successful", "You are now logged in!")
        global current_user_id
        current_user_id = response.json().get('userId')
        login_button.destroy()
        register_button.destroy()
        app.title("Movie Database: Username")
        window.destroy()
    else:
        messagebox.showerror("Register Failed", "User already exists or server error!")


def load_movies(title_filter=None, sort=None):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    if sort == 'Title':
        order = ' ORDER BY title ASC'
    elif sort == 'Year':
        order = ' ORDER BY year ASC'
    else:
        order = ' ORDER BY average_rating DESC'

    if title_filter:
        query = "SELECT movies.id, movies.title, movies.director, movies.actors, movies.year, AVG(ratings.rating_value) AS average_rating FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.title LIKE ? GROUP BY movies.id, movies.title, movies.director, movies.actors, movies.year" + order
        cursor.execute(query, ('%' + title_filter + '%',))
    else:
        query = "SELECT movies.id, movies.title, movies.director, movies.actors, movies.year, AVG(ratings.rating_value) AS average_rating FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id GROUP BY movies.id, movies.title, movies.director, movies.actors, movies.year" + order
        cursor.execute(query)

    movies = cursor.fetchall()
    listbox.delete(0, tk.END)
    movie_list.clear()

    for movie in movies:
        movie_obj = Movie(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5])
        listbox.insert(tk.END, str(movie_obj))  # Insert string representation into the Listbox
        movie_list.append(movie_obj)

    conn.close()


def show_movie_details(index):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movies.title, movies.director, movies.year, AVG(ratings.rating_value) AS average_rating FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.id = ?", (movie_list[index].id,))
    movie = cursor.fetchone()

    if movie:
        title_label.config(text="Title: " + movie[0])
        director_label.config(text="Director: " + movie[1])
        year_label.config(text="Year: " + str(movie[2]))
        average_rating_label.config(text="Average rating: " + str(movie[3]))

    if current_user_id != -1:
        show_rating_buttons(index)

    conn.close()


def show_rating_buttons(index):
    movie_id = movie_list[index].id

    # Function to update the rating
    def set_rating(new_rating):
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()

        # Check if the rating already exists
        cursor.execute("SELECT id FROM ratings WHERE movie_id = ? AND user_id = ?", (movie_id, 1))
        existing_rating = cursor.fetchone()

        if existing_rating is None:
            # Insert new rating
            cursor.execute("INSERT INTO ratings (movie_id, user_id, rating_value) VALUES (?, ?, ?)",
                           (movie_id, 1, new_rating))
        else:
            # Update existing rating
            cursor.execute("UPDATE ratings SET rating_value = ? WHERE movie_id = ? AND user_id = ?",
                           (new_rating, movie_id, 1))

        conn.commit()
        conn.close()

        update_stars()
        show_movie_details(index)

    def update_stars():
        # Clear existing star buttons
        for widget in rating_frame.winfo_children():
            widget.destroy()

        full_star = PhotoImage(file="star-filled.png")
        empty_star = PhotoImage(file="star-bordered.png")

        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()

        cursor.execute("SELECT rating_value FROM ratings WHERE movie_id = ? AND user_id = ?", (movie_id, 1))
        existing_rating = cursor.fetchone()
        current_rating = 0

        if existing_rating is not None:
            current_rating = existing_rating[0]

        star_buttons = []
        for i in range(5):
            star_btn = Button(rating_frame, image=full_star, command=lambda i=i: set_rating(i + 1))  # Corrected lambda
            star_btn.pack(side="left")
            star_buttons.append(star_btn)

        for index, button in enumerate(star_buttons):
            if index < current_rating:
                button.config(image=empty_star)
                button.image = empty_star
            else:
                button.config(image=full_star)
                button.image = full_star

    update_stars()


def on_movie_select(event):
    selection = event.widget.curselection()
    if selection:
        show_movie_details(selection[0])


def search_movies():
    title_filter = search_entry.get()
    sort = sort_var.get()
    load_movies(title_filter, sort)

app = tk.Tk()
app.title("Movie Database")
app.columnconfigure(1, weight=1)
app.rowconfigure(3, weight=1)
app.geometry('570x250')

movie_list = []
current_user_id = -1

# Frames
search_frame = tk.Frame(app)
search_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

listbox_frame = tk.Frame(app)
listbox_frame.grid(row=1, column=0, sticky='ns')

details_frame = tk.Frame(app)
details_frame.grid(row=1, column=1, sticky='nsew')

rating_frame = tk.Frame(app)
rating_frame.grid(row=2, column=0, sticky='nsew')

users_frame = tk.Frame(app)
users_frame.grid(row=3, column=0, sticky='nsew')

sort_frame = tk.Frame(app)
sort_frame.grid(row=2, column=1, sticky='nsew')

# Search area
search_entry = tk.Entry(search_frame, width=50)
search_entry.pack(side=tk.LEFT, padx=10, pady=10)

search_button = tk.Button(search_frame, text="Search Movies", command=lambda: search_movies())
search_button.pack(side=tk.LEFT, padx=10)


# User interaction area in the listbox_frame
login_button = tk.Button(users_frame, text="Login", command=open_login_window)
login_button.pack(side=tk.LEFT, padx=10, pady=10)

register_button = tk.Button(users_frame, text="Register", command=open_register_window)
register_button.pack(side=tk.LEFT, padx=10)

# Dropdown menu for sorting options
sort_options = ['Title', 'Year', 'Average Rating']
sort_var = tk.StringVar(app)
sort_var.set(sort_options[0])  # default value
sort_menu = tk.OptionMenu(search_frame, sort_var, *sort_options, command=lambda _: search_movies())
sort_menu.pack(side=tk.LEFT)


# Listbox area
listbox = tk.Listbox(listbox_frame, height=8, width=50)
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
listbox.bind('<<ListboxSelect>>', lambda event: on_movie_select(event))


# Movie details labels
title_label = tk.Label(details_frame, anchor="w")
title_label.pack(fill='x', pady=(12, 0))

director_label = tk.Label(details_frame, anchor="w")
director_label.pack(fill='x')

year_label = tk.Label(details_frame, anchor="w")
year_label.pack(fill='x')

average_rating_label = tk.Label(details_frame, anchor="w")
average_rating_label.pack(fill='x')

app.mainloop()
