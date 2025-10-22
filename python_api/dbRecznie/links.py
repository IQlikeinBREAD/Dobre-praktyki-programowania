import csv

class Link:
    def __init__(self, movieId, imdbId, tmdbId):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId

def loadLinks(filePath):
    links = []
    with open(filePath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = Link(
                movieId = int(row['movieId']),
                imdbId = row['imdbId'],
                tmdbId = row['tmdbId']
            )
            links.append(link)
    return links