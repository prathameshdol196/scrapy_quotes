

import scrapy
import csv


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
        pages = 0
        with open("data.csv", "a", newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(["Title", "Author", "Tags"])

            for quote in quotes:
                title = quote.css(".text::text").get()
                author = quote.css(".author::text").get()
                tags = quote.css(".tag::text").getall()

                csv_writer.writerow([title, author, ', '.join(tags)])

            pages += 1

        # go to next page
        next_page = response.css(".next>a").attrib["href"]
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        print(f"scraped {pages} pages ######################################################################")


