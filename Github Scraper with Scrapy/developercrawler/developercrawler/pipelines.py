# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class DevelopercrawlerPipeline:
	def __init__(self):
		self.create_connection()
		self.create_table()

	def create_connection(self):
		self.conn = sqlite3.connect("developersearch_db.db")
		self.curr = self.conn.cursor()

	def create_table(self):
		self.curr.execute(
			"""create table if not exists developersearch_tb (
			link text,
			title text,
			description text,
			languages text,
			contributors text,
			watch text,
			stars text,
			forks text
			)"""
		)

	def store_db(self, item):
		self.curr.execute("""
			insert into developersearch_tb values (?,?,?,?,?,?,?,?)
			""", (
				item["link"],
				item["title"],
				item["description"],
		    	item["languages"],
		    	item["contributors"],
		    	item["watch"],
		    	item["stars"],
		    	item["forks"]
				))
		self.conn.commit()

	def process_item(self, item, spider):
		self.store_db(item)
		return item
