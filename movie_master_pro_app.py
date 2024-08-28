import tkinter as tk
from tkinter import ttk
import pandas as pd
import ast

# load the movie data from the CSV file
try:
    df = pd.read_csv('movie_library.csv')
except FileNotFoundError:
    print("Error: CSV file not found. Please check the file path.")
    df = pd.DataFrame()

# Get a list of unique genres from the dataframe
def get_unique_genres(df):
    try:
        genre_set = set()
        # Loop through each genre and add it to the set
        for genres in df['Genre']:
            genre_list = ast.literal_eval(genres)
            genre_set.update(genre_list)
        return sorted(genre_set)
    except (ValueError, SyntaxError) as e:
        print(f"Oops! There was a problem parsing the genres: {e}")
        return []

# Suggest movies based on the genre the user selects   
def suggest_movies(genre):
    try:
        genre = genre.lower()
        # Filter movies that match the selected genre
        suggestions = df[df['Genre'].str.lower().str.contains(genre)]
        
        # Update the text widget with movie details
        details_text.config(state=tk.NORMAL) 
        details_text.delete(1.0, tk.END)
        
        if not suggestions.empty:
            # Pick a random movie from the suggestions
            random_movie = suggestions.sample(n=1).iloc[0]
            
            movie_details = (
                f"{random_movie['Movie Name']}\n"
                f"{random_movie['Year of Release']}   "
                f"{random_movie['Duration']}   "
                f"Rating: {random_movie['IMBD Rating']}\n"
                f"Director: {random_movie['Director']}\n"
                f"Cast: {random_movie['Cast']}\n"
                f"Plot: {random_movie['Plot']}\n"
                f"{'-'*40}\n"
            )
            details_text.insert(tk.END, movie_details)
        else:
            details_text.insert(tk.END, f"Sorry, no movies found for genre: {genre.title()}")
        
        details_text.config(state=tk.DISABLED)
    
    except Exception as e:
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Something went wrong: {e}")
        details_text.config(state=tk.DISABLED)


# Suggest the top 10 movies based on their ratings
def suggest_top_suggestions():
    try:
        top_suggestions = df.sort_values(by='IMBD Rating', ascending=False)
        top_10_suggestions = top_suggestions.head(10)
        
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        
        if not top_10_suggestions.empty:
            # Display details for the top 10 rated movies
            for _, row in top_10_suggestions.iterrows():
                movie_details = (
                    f"{row['Movie Name']}\n"
                    f"{row['Year of Release']}   "
                    f"{row['Duration']}   "
                    f"Rating: {row['IMBD Rating']}\n"
                    f"Director: {row['Director']}\n"
                    f"Cast: {row['Cast']}\n"
                    f"Plot: {row['Plot']}\n"
                    f"{'-'*40}\n"
                )
                details_text.insert(tk.END, movie_details)
        else:
            details_text.insert(tk.END, "No top suggestions available right now.")
        
        details_text.config(state=tk.DISABLED)

    except Exception as e:
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Oops! An error occurred: {e}")
        details_text.config(state=tk.DISABLED)


# Suggest classic movies released before the year 2000
def suggest_classics():
    try:
        classics = df[df['Year of Release'] < 2000]
        classics_sorted = classics.sort_values(by='Year of Release')
        top_classics = classics_sorted.head(10)
        
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        
        if not top_classics.empty:
            # Show details for classic movies
            for _, row in top_classics.iterrows():
                movie_details = (
                    f"{row['Movie Name']}\n"
                    f"{row['Year of Release']}   "
                    f"{row['Duration']}   "
                    f"Rating: {row['IMBD Rating']}\n"
                    f"Director: {row['Director']}\n"
                    f"Cast: {row['Cast']}\n"
                    f"Plot: {row['Plot']}\n"
                    f"{'-'*40}\n"
                )
                details_text.insert(tk.END, movie_details)
        else:
            details_text.insert(tk.END, "No classic movies found.")
        
        details_text.config(state=tk.DISABLED)
    except Exception as e:
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Oops! Something went wrong: {e}")
        details_text.config(state=tk.DISABLED)


# Suggest the most recent movies
def suggest_latest_movies():
    try:
        latest_movies = df.sort_values(by='Year of Release', ascending=False)
        top_latest_movies = latest_movies.head(10)
        
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        
        if not top_latest_movies.empty:
            # Show details for the latest movies
            for _, row in top_latest_movies.iterrows():
                movie_details = (
                    f"{row['Movie Name']}\n"
                    f"{row['Year of Release']}   "
                    f"{row['Duration']}   "
                    f"Rating: {row['IMBD Rating']}\n"
                    f"Director: {row['Director']}\n"
                    f"Cast: {row['Cast']}\n"
                    f"Plot: {row['Plot']}\n"
                    f"{'-'*40}\n"
                )
                details_text.insert(tk.END, movie_details)
        else:
            details_text.insert(tk.END, "No latest movies available.")
        
        details_text.config(state=tk.DISABLED)

    except Exception as e:
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Oops! An error occurred: {e}")
        details_text.config(state=tk.DISABLED)


# Set up the main application window
try:
    root = tk.Tk()
    root.title("Movie Master Pro App")
    root.state('zoomed')
    root.configure(bg='#2c3e50')

    # Title label at the top
    title_label = tk.Label(root, text="\U0001F3A5 Welcome to Movie Master Pro \U0001F3A5", font=("Tahoma", 28, "bold"), bg='#2c3e50', fg='#ecf0f1')
    title_label.pack(pady=10)
    
    # Subtitle label with a brief description
    subtitle_label = tk.Label(root, text="Find and explore your next favorite movie with our curated suggestions based on genres, ratings, and more!", 
                            font=("Tahoma", 14), bg='#2c3e50', fg='#ecf0f1', wraplength=800, justify='center')
    subtitle_label.pack(pady=(0, 20))
  
    main_frame = tk.Frame(root, bg='#2c3e50')
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame, bg='#2c3e50')
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    # Label for genre selection
    select_genre_label = tk.Label(left_frame, text="Choose for Me \U0001F3AC", font=("Tahoma", 12, "bold"), bg='#2c3e50', fg='#ecf0f1')
    select_genre_label.pack(pady=(0, 10))

    # Canvas and scrollbar for genre buttons
    canvas_width = 130 
    canvas = tk.Canvas(left_frame, bg='#2c3e50', width=canvas_width)
    scrollbar = tk.Scrollbar(left_frame, orient='vertical', command=canvas.yview)
    button_frame = tk.Frame(canvas, bg='#2c3e50')

    canvas.create_window((0, 0), window=button_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Get all unique genres and create a button for each
    genres = get_unique_genres(df)

    for i, genre in enumerate(genres):
        btn = ttk.Button(button_frame, text=genre, width=18,
                        command=lambda g=genre: suggest_movies(g))
        btn.grid(row=i, column=0, padx=5, pady=5, sticky='ew')

    button_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Frame for top suggestions
    top_suggestions_frame = tk.Frame(main_frame, bg='#2c3e50')
    top_suggestions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    top_suggestions_frame_label = tk.Label(top_suggestions_frame, text="Top 10 \U00002B50", font=("Tahoma", 12, "bold"), bg='#2c3e50', fg='#ecf0f1')
    top_suggestions_frame_label.pack(pady=(0, 10))  

    # Buttons for high rated, classic, and latest movies
    high_rated_button = ttk.Button(top_suggestions_frame, text="High Rated", width=18,
                                        command=suggest_top_suggestions)
    high_rated_button.pack(pady=5)

    classics_button = ttk.Button(top_suggestions_frame, text="Classics", width=18,
                                command=suggest_classics)
    classics_button.pack(pady=5)

    latest_movies_button = ttk.Button(top_suggestions_frame, text="Latest Movies", width=18,
                                    command=suggest_latest_movies)
    latest_movies_button.pack(pady=5)

    # Frame for displaying movie details
    details_frame = tk.Frame(main_frame, bg='#2c3e50', width=600)
    details_frame.pack(side=tk.LEFT, padx=20, pady=20, expand=True)

    details_label = tk.Label(details_frame, text="Your Next Watch \U0001F37F", font=("Tahoma", 16, "bold"), bg='#2c3e50', fg='#ecf0f1')
    details_label.pack(pady=(10, 10))

    # Text widget for showing movie details
    details_text = tk.Text(details_frame, wrap=tk.WORD, bg='#ecf0f1', fg='#2c3e50', font=("Bodoni MT", 15))
    scrollbar_y = tk.Scrollbar(details_frame, command=details_text.yview)
    details_text.config(yscrollcommand=scrollbar_y.set)

    details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    details_text.config(state=tk.DISABLED)

    # Start the Tkinter main loop
    root.mainloop()
except Exception as e:
    print(f"Oops! There was an issue setting up the app: {e}")
