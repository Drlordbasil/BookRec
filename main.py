import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize


class BookExplorer:
    def __init__(self):
        self.book_data = []

    def scrape_book_data(self, bookstore_urls):
        for url in bookstore_urls:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find_all("div", class_="book")
                for book in books:
                    title = book.find("h3").text.strip()
                    author = book.find("span", itemprop="name").text.strip()
                    genre = book.find("span", class_="genre").text.strip()
                    summary = book.find("div", class_="summary").text.strip()
                    self.book_data.append(
                        {
                            "title": title,
                            "author": author,
                            "genre": genre,
                            "summary": summary,
                        }
                    )
            except (requests.exceptions.RequestException, TimeoutError):
                continue

    def analyze_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        tokens = word_tokenize(text)
        sentiment_score = sia.polarity_scores(" ".join(tokens))
        return sentiment_score["compound"]

    def analyze_book_data(self):
        for book in self.book_data:
            sentiment_score = self.analyze_sentiment(book["summary"])
            book["sentiment"] = sentiment_score

    def get_recommendations(self, user_preferences):
        recommendations = []
        preferred_genre = user_preferences.get("genre", "").lower()
        preferred_author = user_preferences.get("author", "").lower()

        for book in self.book_data:
            if (
                preferred_genre in book["genre"].lower()
                or preferred_author in book["author"].lower()
            ):
                recommendations.append(book)

        return recommendations

    def get_book_details(self, book_title):
        book_title = book_title.lower()
        for book in self.book_data:
            if book_title == book["title"].lower():
                return book

        return None


if __name__ == "__main__":
    book_explorer = BookExplorer()

    # Scrape book data from actual websites
    bookstore_urls = [
        "https://www.examplebookstore1.com/",
        "https://www.examplebookstore2.com/",
    ]
    book_explorer.scrape_book_data(bookstore_urls)

    # Analyze book data
    book_explorer.analyze_book_data()

    # User preferences
    user_preferences = {"genre": "Mystery", "author": "Agatha Christie"}

    # Get personalized book recommendations
    recommendations = book_explorer.get_recommendations(user_preferences)
    if recommendations:
        for book in recommendations:
            print(book["title"])
    else:
        print("No book recommendations found.")

    # Get book details
    book_title = "The Silent Patient"
    book_details = book_explorer.get_book_details(book_title)
    if book_details:
        print(book_details)
    else:
        print("Book not found.")
