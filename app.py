from flask import Flask, render_template, request
from search import search_web

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "index.html",
        query="",
        results=[]
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template(
            "index.html",
            query="",
            results=[]
        )

    results = search_web(query)

    return render_template(
        "index.html",
        query=query,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)

