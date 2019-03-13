import scrapy
from ..items import FirstScrapyItem

class HabrSpider(scrapy.Spider):
    name = "habr"
    allowed_domains = ("habr.com", )
    start_urls = ("https://habr.com/ru/", )
    custom_settings = {}

    # def start_requests(self):
    #     urls = [
    #         'https://habr.com/ru/top/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pages = response.xpath("//ul[@id='nav-pagess']//a[href]").extract()

    def parse_page(self, response):
        post_urls = response.xpath("//a[@class='post__title_link']/@href").extract()
        for url in post_urls:
             yield scrapy.Request(url, callback=self.parse_post)

    def parse_post(self, response):
        title = response.xpath("//span[@class='post__title-text']").extract_first()
        main_body = response.xpath("//div[contains(@class, 'post__body')]")
        description = main_body.xpath("//text()").extract()
        image = main_body.xpath(".//img/@src").extract()
        fields_item = FirstScrapyItem()
        fields_item["title"] = title
        fields_item["image"] = image
        fields_item["description"] = description

        # description = main_body.xpath(".//")
        # print(title,  description, image)
        return fields_item
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
