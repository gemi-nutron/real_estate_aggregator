import scrapy

class OlxSpider(scrapy.Spider):
    name = "olx"
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


        ads_links = response.css('div._70cdfb32 > a::attr(href)').getall()
        for link in ads_links:
            yield response.follow(
                link,
                meta={
                    "playwright": True,
                },
                callback=self.parse_ad
            )

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
    def parse_ad(self, response):

        price = response.css('[aria-label="Price"]::text').get()

        title = response.css('h1._75bce902::text').get()

        yield{

            'ad_url': response.url,

            'title': title,

            'price': price

        } 