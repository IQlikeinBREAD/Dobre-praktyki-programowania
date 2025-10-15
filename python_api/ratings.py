import csv

class Rating:
    def __init__(self, userId, movieId, rating, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp

def loadRatings(filePath):
    ratings = []
    with open(filePath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rating = Rating(
                userId = int(row['userId']),
                movieId = int(row['movieId']),
                rating = float(row['rating']),
                timestamp = int(row['timestamp'])
            )
            ratings.append(rating)
    return ratings