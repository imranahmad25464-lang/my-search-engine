# 🔎 MySearch Engine

A modern web search engine built with Python and Flask that combines local indexed results with web search results in a clean, user-friendly interface.

## 🌐 Live Demo

**[Visit MySearch Engine](https://my-search-engine-fhor.onrender.com/)**

## ✨ Features

- 🔍 Search using custom queries
- 📚 Local search powered by an inverted index
- 🌐 Web search results integration
- 🕷️ Web crawling and indexing
- 🎨 Modern UI with custom background and styling
- 📱 Responsive search interface
- ⚡ Python and Flask backend

## 🛠️ Tech Stack

- Python
- Flask
- Requests
- Beautiful Soup
- HTML5
- CSS3
- JSON
- Gunicorn
- Render

## 📁 Project Structure

```text
my-search-engine/
├── app.py
├── crawler.py
├── indexer.py
├── search.py
├── search_index.json
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── search-bg.jpg
```

## ⚙️ Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/imranahmad25464-lang/my-search-engine.git
   ```

2. Open the project folder:

   ```bash
   cd my-search-engine
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file if your search configuration requires environment variables. Add your own credentials locally; never commit secrets to GitHub.

5. Start the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## 🚀 Deployment

The application is deployed on Render using Gunicorn.

## 🎯 Project Goal

The goal of MySearch Engine is to explore web crawling, indexing, information retrieval, and search result presentation through a practical Python web application.

## 👨‍💻 Author

**Imran Ahmed**

GitHub: [@imranahmad25464-lang](https://github.com/imranahmad25464-lang)

---

If you find this project interesting, consider giving the repository a ⭐.
