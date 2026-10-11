import os
import json
import re
import requests

from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

INDEX_FILE = "search_index.json"


def tokenize(text):
    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}

    try:
        with open(
            INDEX_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return {}


def search_local_index(query):

    index = load_index()

    if not index:
        return []

    query_words = tokenize(query)

    matched_urls = {}

    for word in query_words:

        pages = index.get(
            word,
            []
        )

        for page in pages:

            url = page.get(
                "url",
                ""
            )

            if not url:
                continue

            if url not in matched_urls:

                matched_urls[url] = {
                    "url": url,
                    "title": page.get(
                        "title",
                        "Untitled Page"
                    ),
                    "description": page.get(
                        "description",
                        "No description available."
                    ),
                    "score": 0
                }

            matched_urls[url]["score"] += 1

            # Title match gets extra points
            title = page.get(
                "title",
                ""
            ).lower()

            if word in title:
                matched_urls[url]["score"] += 5

            # Description match gets extra points
            description = page.get(
                "description",
                ""
            ).lower()

            if word in description:
                matched_urls[url]["score"] += 2

    results = list(
        matched_urls.values()
    )

    for result in results:

        result["source"] = (
            "MySearch Index"
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


def calculate_score(
    result,
    query
):

    score = 0

    query_words = tokenize(
        query
    )

    title = result.get(
        "title",
        ""
    ).lower()

    description = result.get(
        "description",
        ""
    ).lower()

    url = result.get(
        "url",
        ""
    ).lower()

    for word in query_words:

        if word in title:
            score += 5

        if word in description:
            score += 2

        if word in url:
            score += 1

    if query.lower() in title:
        score += 10

    return score


def search_tavily(query):

    if not TAVILY_API_KEY:

        print(
            "TAVILY API KEY NOT FOUND"
        )

        return []

    url = (
        "https://api.tavily.com/search"
    )

    payload = {

        "api_key": TAVILY_API_KEY,

        "query": query,

        "search_depth": "basic",

        "max_results": 10,

        "include_answer": False
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get(
            "results",
            []
        ):

            result = {

                "title": item.get(
                    "title",
                    "Untitled"
                ),

                "url": item.get(
                    "url",
                    "#"
                ),

                "description": item.get(
                    "content",
                    "No description available."
                ),

                "source": "Web Search"
            }

            result["score"] = (
                calculate_score(
                    result,
                    query
                )
            )

            results.append(
                result
            )

        return results

    except Exception as error:

        print(
            "TAVILY ERROR:",
            error
        )

        return []


def remove_duplicates(results):

    unique_results = []

    seen_urls = set()

    for result in results:

        url = result.get(
            "url",
            ""
        )

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        unique_results.append(
            result
        )

    return unique_results


def search_web(query):

    print(
        "\n========== MYSEARCH =========="
    )

    print(
        "Query:",
        query
    )

    # Own index
    local_results = (
        search_local_index(
            query
        )
    )

    # Web search
    tavily_results = (
        search_tavily(
            query
        )
    )

    # Combine
    all_results = (
        local_results
        + tavily_results
    )

    # Remove duplicates
    all_results = (
        remove_duplicates(
            all_results
        )
    )

    # Smart ranking
    all_results.sort(
        key=lambda x: x.get(
            "score",
            0
        ),
        reverse=True
    )

    print(
        "Local results:",
        len(local_results)
    )

    print(
        "Web results:",
        len(tavily_results)
    )

    print(
        "Final results:",
        len(all_results)
    )

    print(
        "=============================="
    )

    return all_results[:15]