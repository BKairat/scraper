# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class FlatsScraperPipeline:
    def __init__(self):
        hostname = 'postgres'
        username = 'user_test'
        password = '12345'
        database = 'flats'

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        self.cur = self.connection.cursor()
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS parsed_flats(
            id serial PRIMARY KEY, 
            title VARCHAR,
            image VARCHAR
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(""" insert into parsed_flats (title, image) values (%s,%s)""", (
            item["title"],
            item["image"]
        ))

        self.connection.commit()
        return item

    def close_spider(self, spider): 
        self.cur.close()
        self.connection.close()
