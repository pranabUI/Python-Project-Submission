The Movie Master Pro App project is a two-part application developed in Python, combining web scraping, data processing, and a graphical user interface (GUI) to create a dynamic and interactive movie recommendation tool. The project aims to provide users with curated movie suggestions based on genres, IMDb ratings, release years, and other attributes, enhancing the movie-watching experience by making it easier to discover new films.

**imdb_movie_scraper program**


The first Python program is designed to build a bot that scrapes data from IMDb to suggest movies based on user preferences. This program specifically scrapes the IMDb Top 250 movies page to extract movie details, including movie names, release years, durations, genres, IMDb ratings, directors, main cast members, plots, and poster URLs. It then stores the scraped data in a CSV file for further use or analysis.

Components:
1. Using requests and BeautifulSoup to access IMDb's Top 250 movies page and extract detailed movie information such as names, release years, durations, genres, IMDb ratings, directors, top cast members, plots, and poster URLs.
2. Converting movie durations from ISO 8601 format to a human-readable form and handling missing or malformed data.
3. Storing the cleaned data in a Pandas DataFrame and exporting it to a CSV file (movie_library.csv) for easy access in subsequent steps.
4. Implementing error handling to manage potential issues with HTTP requests and JSON parsing, ensuring robustness and reliability.

**movie_master_pro_app program**


The second Python program provides a graphical user interface (GUI) for the movie suggestion app using tkinter. It leverages the movie data extracted from IMDb and saved in a CSV file (from the first program) to allow users to explore and select movies based on genres, ratings, release years, and more.

Components:
1. Reading the previously saved movie_library.csv file into a Pandas DataFrame.
2. Extracting unique genres from the data and dynamically generating buttons in the GUI for each genre, allowing users to select their preferred genre.
3. Using tkinter for the GUI, with frames, labels, buttons, and text widgets to create a visually appealing and user-friendly interface.
4. Implementing error handling to manage issues related to data loading, parsing, and GUI operations.

Libraries Used: 
1. requests - For sending HTTP requests to fetch HTML content from IMDb pages.
2. BeautifulSoup - For parsing HTML content to extract structured data embedded in the page.
3. re - For using regular expressions to parse movie durations and convert them to a human-readable format.
4. pandas - For creating DataFrames to store the extracted movie details and exporting them to a CSV file.
5. tkinter - For creating the graphical user interface. It provides the main window, frames, labels, buttons, and text widgets for displaying content.
6. ttk  - For themed widgets to enhance the GUI's visual style.
7. ast - For safely evaluating string representations of Python data structures (e.g., converting genre strings back to lists).
8. json - For decoding JSON-LD data embedded in IMDb pages.

App Features:
1. Users can select a genre from a dynamically generated list of buttons. When a button is clicked, a random movie suggestion from that genre is displayed in the app.
2. Displays the top 10 movies sorted by IMDb rating.
3. Shows classic movies released before the year 2000, sorted by their release year.
4. Suggests the most recent movies by showing the top 10 latest releases.
