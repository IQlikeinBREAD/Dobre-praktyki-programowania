from python_api.sql.DBSQLite import Base, engine
from python_api.sql.models import Movie, Link, Rating, Tag

Base.metadata.create_all(bind=engine)
print("Database and tables created.")