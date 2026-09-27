from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_movies(
        selected_title,
        movies,
        minimum_similarity=0.5
):
    selected_index = None

    for index, movie in enumerate(movies):
        if movie["title"].lower() == selected_title.lower():
            selected_index = index
            break

    if selected_index is None:
        return []

    movie_texts = []

    for movie in movies:
        genres = " ".join(movie["genres"])
        text = movie["overview"] + " " + genres
        movie_texts.append(text)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(movie_texts)

    similarities = cosine_similarity(
        tfidf_matrix[selected_index],
        tfidf_matrix
    ).flatten()

    sorted_indices = similarities.argsort()[::-1]

    recommendations = []

    for index in sorted_indices:
        movie = movies[index]
        similarity = similarities[index]

        if index == selected_index:
            continue

        if movie["title"].lower() == selected_title.lower():
            continue

        if similarity > minimum_similarity:
            recommendations.append(movie["title"])

    return recommendations