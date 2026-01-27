
import pytest


def test_get_movies_by_id(client, admin_headers):
    response = client.get("/movies/123", headers=admin_headers)

    assert response.status_code == 200

    movie = response.json()
    assert movie["movieId"] == 123
    assert movie["title"] == "Pony"
    assert movie["genres"] == "Fantasy"

def test_get_movies_by_id_not_found(client, admin_headers):
    response = client.get("/movies/999", headers=admin_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}