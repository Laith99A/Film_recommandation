from flask import Flask, render_template, request

from recommender import build_tfidf_matrix, find_similar_movies
from sparql_queries import get_all_movies


app = Flask(__name__)

# Loaded from Fuseki only once (on the first search) and then
# reused for every following search.
movies = None
tfidf_matrix = None


def load_movie_data():
    global movies, tfidf_matrix

    if movies is None:
        loaded_movies = get_all_movies()
        tfidf_matrix = build_tfidf_matrix(loaded_movies)
        movies = loaded_movies

    return movies, tfidf_matrix


def find_movie_index(title, movies):
    for index, movie in enumerate(movies):
        if movie["title"].lower() == title.lower():
            return index

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    selected_movie = None
    genres = []
    similar_movies = []
    error_message = None
    searched_title = ""

    if request.method == "POST":
        searched_title = request.form.get("title", "").strip()

        if not searched_title:
            error_message = "Please enter a movie title."

        else:
            movies, tfidf_matrix = load_movie_data()
            movie_index = find_movie_index(searched_title, movies)

            if movie_index is None:
                error_message = (
                    f'The movie "{searched_title}" was not found '
                    "in the database."
                )

            else:
                movie = movies[movie_index]
                selected_movie = movie["title"]
                genres = movie["genres"]

                similar_movies = find_similar_movies(
                    selected_index=movie_index,
                    movies=movies,
                    tfidf_matrix=tfidf_matrix,
                    minimum_similarity=0.1
                )

    return render_template(
        "index.html",
        selected_movie=selected_movie,
        genres=genres,
        similar_movies=similar_movies,
        error_message=error_message,
        searched_title=searched_title
    )


if __name__ == "__main__":
    app.run(debug=True)
