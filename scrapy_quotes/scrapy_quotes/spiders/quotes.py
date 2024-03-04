import scrapy
import json \


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/",
            "https://quotes.toscrape.com/page/2/",
            "https://quotes.toscrape.com/page/3/",
            "https://quotes.toscrape.com/page/4/",
            "https://quotes.toscrape.com/page/5/",
            "https://quotes.toscrape.com/page/6/",
            "https://quotes.toscrape.com/page/7/",
            "https://quotes.toscrape.com/page/8/",
            "https://quotes.toscrape.com/page/9/",
            "https://quotes.toscrape.com/page/10/"

        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css(".quote")

        quotes_data = []

        json_data = json.dumps(quotes_data, indent=4)

        with open("data.json", "w") as json_file:
            json_file.write(json_data)

        for quote in quotes:
            title = quote.css(".text::text").get()
            author = quote.css(".author::text").get()
            tags = quote.css(".tag::text").getall()

            data = {
                "title": title,
                "author": author,
                "tags": tags
            }

            quotes_data.append(data)


