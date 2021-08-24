import scrapy
import urllib.request
from ..items import DevelopercrawlerItem
import sqlite3
import numpy as np
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class DeveloperSearchSpider(CrawlSpider):
    name = "spider"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/topics"]
    base_url = "https://github.com/"

    rules = [Rule(LinkExtractor(deny=("topics", "trending", "about", "features", "sponsors", "collections", "sponsors/community", "azure", "contact", "settings", "marketplace")), callback="parse_link", process_links="process_links", follow=True)]
    running = False

    def process_links(self, links):
        if self.running == False:
            self.create_connection()
            self.create_table()

        crawled = self.get_db()
        print("crawled:    "+str(len(crawled)))
        for link in links:
            length = len(link.url.replace("https://github.com/", "").split("/"))
            if link.url in crawled and length != 2:
                continue
            yield link


    def parse_link(self, response):

        items = DevelopercrawlerItem()
        link = response.request.url
        crawled = self.get_db()
        length = len(link.replace("https://github.com/", "").split("/"))

        if link not in crawled and length == 2:

            title = response.css("#readme h1::text").extract()
            title = "".join(title)

            description = response.css("p::text").extract()
            description = " ".join(description)

            languages = response.css("span.text-gray-dark.text-bold.mr-1::text").extract()
            languages = "#%#".join(languages)

            contributors = response.css(".BorderGrid-row:nth-child(5) .Counter::text").extract()
            contributors = " ".join(contributors)

            watch = response.css("li:nth-child(1) .social-count::text").extract()
            watch = " ".join(watch)

            stars = response.css(".js-social-count::text").extract()
            stars = " ".join(stars)

            forks = response.css("li~ li+ li .social-count::text").extract()
            forks = " ".join(forks)

            if title!="" and description!="" and languages!="" and contributors!="" and watch!="" and stars!="" and forks!="":
                items["link"] = link
                items["title"] = title
                items["description"] = description
                items["languages"] = languages
                items["contributors"] = contributors
                items["watch"] = watch
                items["stars"] = stars
                items["forks"] = forks

                self.store_db(str(link))

                yield items

            elif title!="" or description!="" or languages!="" or contributors!="" or watch!="" or stars!="" or forks!="":
                print("                           partially scraped:             "+link)
                items["link"] = link
                items["title"] = title
                items["description"] = description
                items["languages"] = languages
                items["contributors"] = contributors
                items["watch"] = watch
                items["stars"] = stars
                items["forks"] = forks

                self.store_db(str(link))

                yield items

    def create_connection(self):
        self.conn = sqlite3.connect("crawledurls_db.db")
        self.curr = self.conn.cursor()
        self.running = True

    def create_table(self):
        self.curr.execute(
            """create table if not exists crawledurls_tb (
            link text
            )""")
        
    def store_db(self, link):
        self.curr.execute("insert into crawledurls_tb values (?)", (link,))
        self.conn.commit()

    def get_db(self):
        self.curr.execute('SELECT * FROM crawledurls_tb')
        result = self.curr.fetchall()
        result = np.asarray(result).flatten()
        return result
    
