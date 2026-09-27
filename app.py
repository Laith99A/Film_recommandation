from flask import Flask, render_template, request

from recommender import find_similar_movies
from sparql_queries import get_all_movies, get_movie


app = Flask(__name__)


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
            movie = get_movie(searched_title)

            if movie is None:
                error_message = (
                    f'The movie "{searched_title}" was not found '
                    "in the database."
                )

            else:
                selected_movie = movie["title"]
                genres = movie["genres"]

                all_movies = get_all_movies()

                similar_movies = find_similar_movies(
                    selected_title=selected_movie,
                    movies=all_movies,
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