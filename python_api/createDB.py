from DBSQLite import Base, engine
from models import Movie, Link, Rating, Tag

Base.metadata.create_all(bind=engine)
print("Database and tables created.")