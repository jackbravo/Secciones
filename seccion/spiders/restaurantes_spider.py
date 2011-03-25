from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from seccion.items import RestauranteItem

class RestaurantesSpider(BaseSpider):
    name = "restaurantes"
    allowed_domains = ["seccionamarilla.com"]
    start_urls = [
        "http://www.seccionamarilla.com.mx/Resultados/restaurantes/jalisco/guadalajara/1"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//div[@id="marco"]')
        items = []
        for result in results:
            item = RestauranteItem()
            item['name'] = result.select('.//a[@class="anclas"]/text()').extract()
            item['category'] = result.select('.//td[@class="categoria"]/a/text()').extract()
            items.append(item)
        return items
