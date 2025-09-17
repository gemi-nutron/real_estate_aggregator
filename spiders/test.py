import scrapy

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.dubizzle.com.eg"]

    def start_requests(self):
        url = 'https://www.dubizzle.com.eg/en/properties/'
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
            },
            callback=self.parse
        )

    def parse(self, response):
        next_page = response.xpath('//a[div/@title="Next"]/@href').get()
        
        if next_page is not None:
            self.logger.info(f"Next page found, following to: {next_page}")
            yield response.follow(
                next_page,
                meta={
                    "playwright": True,
                },
                callback=self.parse
            )
        else:
            self.logger.info("No more pages to follow. Spider finished.")