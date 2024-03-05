import scrapy
import os
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define the SQLAlchemy engine and create a session
engine = create_engine(f'mysql+mysqlconnector://{os.environ["mysql_user"]}:{os.environ["mysql_pass"]}@localhost')

# Create the database if it doesn't exist
engine.execute("CREATE DATABASE IF NOT EXISTS quotes")
engine.execute("USE quotes")

# Define a base class for declarative class definitions
Base = declarative_base()


# Define a simple table
class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    author = Column(String(255))
    tags = Column(String(255))


# Creates table in db
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

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

            # Create a new Quote instance
            new_quote = Quote(title=title, author=author, tags=', '.join(tags))
            session.add(new_quote)

            session.commit()

        # go to next page
        next_page = response.css(".next>a").attrib["href"]
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
