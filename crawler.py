import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}


def crawl_page(url):
    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(
                " ",
                strip=True
            )

        description = ""

        meta_description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_description:
            description = meta_description.get(
                "content",
                ""
            )

        content = soup.get_text(
            " ",
            strip=True
        )

        content = " ".join(
            content.split()
        )

        links = []

        base_domain = urlparse(url).netloc

        for anchor in soup.find_all(
            "a",
            href=True
        ):

            link = urljoin(
                url,
                anchor["href"]
            )

            parsed = urlparse(link)

            if (
                parsed.scheme in ["http", "https"]
                and parsed.netloc == base_domain
            ):

                clean_link = (
                    parsed.scheme
                    + "://"
                    + parsed.netloc
                    + parsed.path
                )

                if clean_link not in links:
                    links.append(clean_link)

        return {
            "url": url,
            "title": title,
            "description": description,
            "content": content[:10000],
            "links": links[:30]
        }

    except Exception as error:

        print(
            "CRAWL ERROR:",
            url,
            error
        )

        return None


def crawl_website(start_url, max_pages=5):

    visited = set()
    queue = [start_url]
    pages = []

    while queue and len(pages) < max_pages:

        current_url = queue.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        print(
            f"\nCrawling page {len(pages) + 1}/{max_pages}:"
        )

        print(current_url)

        page = crawl_page(
            current_url
        )

        if not page:
            continue

        pages.append(page)

        for link in page["links"]:

            if (
                link not in visited
                and link not in queue
                and len(queue) < max_pages * 3
            ):

                queue.append(link)

    return pages


if __name__ == "__main__":

    start_url = "https://www.python.org/"

    pages = crawl_website(
        start_url,
        max_pages=5
    )

    print(
        "\n========== CRAWLER RESULT =========="
    )

    print(
        "Total pages crawled:",
        len(pages)
    )

    for page in pages:

        print(
            "\nTitle:",
            page["title"]
        )

        print(
            "URL:",
            page["url"]
        )

        print(
            "Links found:",
            len(page["links"])
        )

    print(
        "\nMulti-page crawler working successfully!"
    )