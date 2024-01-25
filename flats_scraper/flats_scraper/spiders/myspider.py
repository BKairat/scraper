from flats_scraper.items import FlatsScraperItem
import scrapy

class FlatsSpider(scrapy.Spider):
    name = "flats"
    start_urls = [f'https://www.sreality.cz/hledani/prodej/byty?strana={p}' for p in range(26)]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(
                url=url,
                meta={"playwright": True},
            )

    def parse(self, response, **kwargs):
        ads = response.xpath('//div[@class="property ng-scope"]')
        flat_item = FlatsScraperItem()
        for ad in ads:
            title = ad.xpath('.//span[@class="name ng-binding"]/text()').get()
            image = ad.xpath('.//img/@src').extract()[0]
            flat_item["title"] = title
            flat_item["image"] = image
            yield flat_item
