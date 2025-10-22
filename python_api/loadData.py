import csv
from DBSQLite import SessionLocal
from models import Movie, Link, Rating, Tag

def loadMovies(db):
    with open("data_base/movies.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = Movie(
                movieId=int(row['movieId']),
                title=row['title'],
                genres=row['genres']
            )
            db.add(movie)
    db.commit()

def loadLinks(db):
    with open("data_base/links.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            link = Link(
                movieId=int(row['movieId']),
                imdbId=int(row['imdbId']) if row['imdbId'] else None,
                tmdbId=int(row['tmdbId']) if row['tmdbId'] else None
            )
            db.add(link)
    db.commit()

def loadRatings(db):
    with open("data_base/ratings.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rating = Rating(
                userId=int(row['userId']),
                movieId=int(row['movieId']),
                rating=float(row['rating']),
                timestamp=int(row['timestamp'])
            )
            db.add(rating)
    db.commit()

def loadTags(db):
    with open("data_base/tags.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tag = Tag(
                userId=int(row['userId']),
                movieId=int(row['movieId']),
                tag=row['tag'],
                timestamp=int(row['timestamp'])
            )
            db.add(tag)
    db.commit()

def main():
    db = SessionLocal()
    loadMovies(db)
    loadLinks(db)
    loadRatings(db)
    loadTags(db)
    db.close()

if __name__ == "__main__":
    main()