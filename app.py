from urllib.error import URLError

from flask import Flask, render_template, request
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound

from movie_search import search_movie
from recommender import build_tfidf_matrix, find_similar_movies
from sparql_queries import get_all_movies


app = Flask(__name__)

# Loaded from Fuseki only once (when the page is first opened) and
# then reused for every following search.
cached_movies = None
cached_tfidf_matrix = None


class MovieDatabaseError(Exception):
    pass


def load_movie_data():
    global cached_movies, cached_tfidf_matrix

    if cached_movies is None:
        try:
            movies = get_all_movies()

        except EndPointNotFound:
            raise MovieDatabaseError(
                "Fuseki is running, but the dataset TMDB was not found. "
                "Create it at http://localhost:3030 and upload tmdb.ttl."
            )

        except URLError:
            raise MovieDatabaseError(
                "Could not connect to the movie database. "
                "Please start Fuseki (http://localhost:3030) "
                "with the dataset TMDB."
            )

        # An empty dataset is not cached, so the movies are loaded
        # again on the next request (e.g. after uploading tmdb.ttl).
        if not movies:
            raise MovieDatabaseError(
                "The dataset TMDB contains no movies. "
                "Upload tmdb.ttl at http://localhost:3030."
            )

        cached_tfidf_matrix = build_tfidf_matrix(movies)
        cached_movies = movies

    return cached_movies, cached_tfidf_matrix


@app.route("/")
def index():
    selected_movie = None
    genres = []
    similar_movies = []
    suggestions = []
    all_titles = []
    error_message = None
    searched_title = request.args.get("title", "").strip()

    try:
        movies, tfidf_matrix = load_movie_data()
        all_titles = sorted(set(movie["title"] for movie in movies))

    except MovieDatabaseError as error:
        error_message = str(error)

    # "title" is only in the URL after the form was submitted
    if error_message is None and "title" in request.args:
        if not searched_title:
            error_message = "Please enter a movie title."

        else:
            movie_index, suggestions = search_movie(searched_title, movies)

            if movie_index is not None:
                movie = movies[movie_index]
                selected_movie = movie["title"]
                genres = movie["genres"]

                similar_movies = find_similar_movies(
                    selected_index=movie_index,
                    movies=movies,
                    tfidf_matrix=tfidf_matrix,
                    minimum_similarity=0.1
                )

            elif not suggestions:
                error_message = (
                    f'The movie "{searched_title}" was not found '
                    "in the database."
                )

    return render_template(
        "index.html",
        selected_movie=selected_movie,
        genres=genres,
        similar_movies=similar_movies,
        suggestions=suggestions,
        all_titles=all_titles,
        error_message=error_message,
        searched_title=searched_title
    )


if __name__ == "__main__":
    app.run(debug=True)
