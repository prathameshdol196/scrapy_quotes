import scrapy
import os
import mysql.connector


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user=os.environ["mysql_user"],
            password=os.environ["mysql_pass"]
        )

        self.cursor = self.connection.cursor()

        # Create db if not exist
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS quotes")

        self.connection.database = 'quotes'

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS quotes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title TEXT,
                            author VARCHAR(255),
                            tags TEXT
                        )
                    """)

        self.connection.commit()

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        quotes = response.css(".quote")

        for quote in quotes:
            title = quote.css(".text::text").get()
            author = quote.css(".author::text").get()
            tags = quote.css(".tag::text").getall()

            sql = "INSERT INTO quotes (title, author, tags) VALUES (%s, %s, %s)"
            val = (title, author, ', '.join(tags))

            self.cursor.execute(sql, val)
            self.connection.commit()

        # go to next page
        next_page = response.css(".next>a").attrib["href"]
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
