from SPARQLWrapper import SPARQLWrapper, JSON


SPARQL_ENDPOINT = "http://localhost:3030/TMDB/sparql"


def get_movie(title):
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')

    query = f"""
    PREFIX : <https://www.themoviedb.org/kaggle-export/>

    SELECT ?title ?overview
           (GROUP_CONCAT(DISTINCT ?genreName; separator="|") AS ?genres)
    WHERE {{
        ?movie a :Movie ;
               :title ?title ;
               :genres ?genre .

        ?genre :name ?genreName .

        OPTIONAL {{
            ?movie :overview ?overview .
        }}

        FILTER(LCASE(STR(?title)) = LCASE("{safe_title}"))
    }}
    GROUP BY ?title ?overview
    LIMIT 1
    """

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    rows = result["results"]["bindings"]

    if not rows:
        return None

    row = rows[0]

    genres_text = row.get("genres", {}).get("value", "")

    return {
        "title": row["title"]["value"],
        "overview": row.get("overview", {}).get("value", ""),
        "genres": genres_text.split("|") if genres_text else []
    }
def get_all_movies():
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/>

    SELECT ?movie ?title ?overview
           (GROUP_CONCAT(DISTINCT ?genreName; separator="|") AS ?genres)
    WHERE {
        ?movie a :Movie ;
               :title ?title ;
               :overview ?overview .

        OPTIONAL {
            ?movie :genres ?genre .
            ?genre :name ?genreName .
        }

        FILTER(STRLEN(STR(?overview)) > 0)
    }
    GROUP BY ?movie ?title ?overview
    """

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    rows = result["results"]["bindings"]

    movies = []

    for row in rows:
        genres_text = row.get("genres", {}).get("value", "")

        movies.append({
            "uri": row["movie"]["value"],
            "title": row["title"]["value"],
            "overview": row["overview"]["value"],
            "genres": genres_text.split("|") if genres_text else []
        })

    return movies