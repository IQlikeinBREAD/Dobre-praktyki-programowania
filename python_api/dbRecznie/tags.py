import csv

class Tag:
    def __init__(self, userId, movieId, tag, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp

def loadTags(filePath):
    tags = []
    with open(filePath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = Tag(
                userId = int(row['userId']),
                movieId = int(row['movieId']),
                tag = row['tag'],
                timestamp = int(row['timestamp'])
            )
            tags.append(tag)
    return tags