import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd

def fetch_movie_details(url, headers, num_movies=None):
    try:
        # Sending request and parsing HTML content to extract JSON-LD data of main page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        data = json.loads(soup.find('script', {'type': "application/ld+json"}).text)

        # Getting the maximum number of movies available in page
        if num_movies is None:
            num_movies = len(data['itemListElement'])

        # Initializing an empty list to store details of each movie
        movies = []

        # Looping through the movies, fetching details, and parsing information
        for item in data['itemListElement'][:num_movies]:
            movie_url = item['item']['url']

            try:
                # Sending request and parsing HTML content to extract JSON-LD data of movie's page
                movie_response = requests.get(movie_url, headers=headers)
                movie_response.raise_for_status()  # Raise an HTTPError for bad responses
                movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
                movie_data = json.loads(movie_soup.find('script', {'type': "application/ld+json"}).text)
                
                # Extracting movie name & release year
                movie_name = movie_data['name']
                release_date = movie_data['datePublished'][:4] if 'datePublished' in movie_data else "N/A"
                
                # Converting movie duration to a readable format
                if 'duration' in movie_data:
                    duration_before = movie_data['duration']
                    match = re.match(r'PT(\d*)H(\d*)M', duration_before)
                    if match:
                        hours = match.group(1) or '0'
                        minutes = match.group(2) or '0'
                        duration = f"{hours}h {minutes}m"
                    else:
                        duration = "N/A"
                else:
                    duration = "N/A"

                # Extracting genre, rating & director
                genre = movie_data['genre'] if 'genre' in movie_data else "N/A"
                rating = movie_data['aggregateRating']['ratingValue'] if 'aggregateRating' in movie_data and 'ratingValue' in movie_data['aggregateRating'] else "N/A"
                director = movie_data['director'][0]['name'] if 'director' in movie_data and movie_data['director'] else "N/A"
                
                # Extracting names of top 3 actors
                if 'actor' in movie_data and movie_data['actor']:
                    actors = [actor['name'] for actor in movie_data['actor'][:3]]
                    actor_names = ', '.join(actors) 
                else:
                    actor_names = "N/A"
                
                # Extracting plot
                description = movie_data['description'] if 'description' in movie_data else "N/A"

                # Appending the extracted details as a dictionary to the movies list
                movies.append({
                    'Movie Name': movie_name,
                    'Year of Release': release_date,
                    'Duration': duration,
                    'Genre': genre,
                    'IMBD Rating': rating,
                    'Director': director,
                    'Cast': actor_names,
                    'Plot': description
                })

            except (requests.RequestException, json.JSONDecodeError) as e:
                print(f"Error fetching or parsing data for movie URL {movie_url}: {e}")
                continue  # Skip this movie and continue with the next one

        return movies

    except (requests.RequestException, json.JSONDecodeError, AttributeError) as e:
        print(f"Error fetching or parsing main page data: {e}")
        return []

# Custom headers to mimic a real browser request
headers = {
    'Accept': '*/*', 
    'Connection': 'keep-alive', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 
    'Accept-Language': 'en-US;q=0.5,en;q=0.3', 
    'Cache-Control': 'max-age=0', 
    'Upgrade-Insecure-Requests': '1'
}

# URL of IMDb's Top 250 movies page
url = 'https://www.imdb.com/chart/top/'

# Fetching movie details dynamically
movie_details = fetch_movie_details(url, headers)

try:
    # Converting the list of movie dictionaries into a Pandas DataFrame
    df = pd.DataFrame(movie_details)

    # Exporting the DataFrame to a CSV file
    file_name = "movie_library.csv"
    df.to_csv(file_name, index=False)

    # Printing the number of movies found and exported
    num_movies_found = len(df)
    print(f"Data has been exported to {file_name}.\nNumber of movies found: {num_movies_found}")

except Exception as e:
    print(f"Error exporting data to CSV: {e}")
