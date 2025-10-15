import csv

class Movie:
    def __init__(self, id, title, genres):
        self.id = id
        self.tittle = title
        self.genres = genres
    

def load_movies(filePath):
    movies = []
    with open(filePath, newline='', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index,row in enumerate(reader,start=1):
            movie = Movie(
                id = index,
                title = row['title'],
                genres = row['genres']
            )
            movies.append(movie)
    return movies