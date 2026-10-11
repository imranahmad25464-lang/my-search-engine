import json
import os
import re

from crawler import crawl_website


INDEX_FILE = "search_index.json"


def tokenize(text):
    text = text.lower()

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text
    )


def create_index(pages):
    """
    Create a searchable index with
    page title, description and URL.
    """

    index = {}

    for page in pages:

        url = page.get("url", "")

        page_data = {
            "url": url,
            "title": page.get(
                "title",
                "Untitled Page"
            ),
            "description": page.get(
                "description",
                "No description available."
            )
        }

        text = (
            page.get("title", "")
            + " "
            + page.get("description", "")
            + " "
            + page.get("content", "")
        )

        words = tokenize(text)

        for word in words:

            if word not in index:
                index[word] = []

            already_exists = False

            for existing in index[word]:

                if existing["url"] == url:
                    already_exists = True
                    break

            if not already_exists:
                index[word].append(
                    page_data
                )

    return index


def save_index(index):

    with open(
        INDEX_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            index,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nIndex saved to {INDEX_FILE}"
    )


def load_index():

    if not os.path.exists(
        INDEX_FILE
    ):
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


def build_search_index(
    start_url,
    max_pages=5
):

    print(
        "\nStarting multi-page crawler..."
    )

    pages = crawl_website(
        start_url,
        max_pages=max_pages
    )

    if not pages:

        print(
            "\nNo pages were crawled."
        )

        return {}

    print(
        "\nCreating metadata-based index..."
    )

    index = create_index(
        pages
    )

    save_index(
        index
    )

    print(
        "\nPages indexed:",
        len(pages)
    )

    print(
        "Total indexed words:",
        len(index)
    )

    return index


if __name__ == "__main__":

    print(
        "\n===================================="
    )

    print(
        "       MYSEARCH METADATA INDEXER"
    )

    print(
        "===================================="
    )

    start_url = "https://www.python.org/"

    index = build_search_index(
        start_url,
        max_pages=5
    )

    if index:

        print(
            "\n========== INDEX SAMPLE =========="
        )

        sample_word = list(
            index.keys()
        )[0]

        print(
            "\nWord:",
            sample_word
        )

        print(
            "\nStored page data:"
        )

        for page in index[sample_word]:

            print(
                "\nTitle:",
                page["title"]
            )

            print(
                "URL:",
                page["url"]
            )

            print(
                "Description:",
                page["description"]
            )

        print(
            "\n===================================="
        )

        print(
            "Metadata indexer working successfully!"
        )

        print(
            "===================================="
        )

    else:

        print(
            "\nIndexer failed."
        )