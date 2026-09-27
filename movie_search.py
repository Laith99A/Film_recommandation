import difflib


def search_movie(query, movies, max_suggestions=10):
    """
    Returns (movie_index, suggestions).

    movie_index is the position of the found movie in `movies`, or None
    if there is no clear match. suggestions is a list of titles the user
    may have meant.
    """
    query = query.lower()

    # 1. Exact title (upper/lower case does not matter)
    for index, movie in enumerate(movies):
        if movie["title"].lower() == query:
            return index, []

    # 2. Titles that contain the search text, e.g. "dead" -> "Deadpool".
    # Movies with the same title are only listed once.
    first_index_by_title = {}

    for index, movie in enumerate(movies):
        title = movie["title"]

        if query in title.lower() and title not in first_index_by_title:
            first_index_by_title[title] = index

    if len(first_index_by_title) == 1:
        return list(first_index_by_title.values())[0], []

    if first_index_by_title:
        # Titles that start with the search text first, then the
        # shortest titles, because they are usually the closest match
        matching_titles = sorted(
            first_index_by_title,
            key=lambda title: (
                not title.lower().startswith(query),
                len(title),
                title
            )
        )

        return None, matching_titles[:max_suggestions]

    # 3. Similar spelling, e.g. the typo "titanc" -> "Titanic"
    titles_by_lowercase = {}

    for movie in movies:
        titles_by_lowercase.setdefault(movie["title"].lower(), movie["title"])

    close_matches = difflib.get_close_matches(
        query,
        list(titles_by_lowercase),
        n=max_suggestions,
        cutoff=0.6
    )

    return None, [titles_by_lowercase[match] for match in close_matches]
