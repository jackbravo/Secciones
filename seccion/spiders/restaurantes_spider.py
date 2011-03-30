from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from seccion.items import RestauranteItem

class RestaurantesSpider(BaseSpider):
    name = "restaurantes"
    allowed_domains = ["seccionamarilla.com.mx"]
    start_urls = [
        "http://www.seccionamarilla.com.mx/Resultados/restaurantes/jalisco/guadalajara/1"
    ]
    position = 0

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for result in hxs.select('//div[@id="marco"]'):
            item = RestauranteItem()
            item['name'] = self.pop_or_nil(result.select('.//a[@class="anclas"]/text()').extract())
            item['full_url'] = self.pop_or_nil(result.select('.//a[@class="anclas"]/@href').extract())
            item['category'] = self.pop_or_nil(result.select('.//td[@class="categoria"]/a/text()').extract())
            item['address'] = self.pop_or_nil(result.select('.//tr[3]//strong/text()').extract())
            item['phone'] = self.pop_or_nil(result.select('.//span[@class="tellist"]/text()').extract())
            star_url = 'http://images.seccionamarilla.com.mx/rating/estrella.gif'
            item['rating'] = len(result.select('.//img[@src="' + star_url + '"]'))
            item['num_reviews'] = self.pop_or_nil(result.select('.//div[@id="rating"]//font//text()').re('(\d+)'))
            if (result.select('.//div[@id="contlist_lpt"]').extract()):
                item['result_type'] = 'sponsored'
            elif (result.select('.//div[@class="td_lista_result_Diamante"]').extract()):
                item['result_type'] = 'diamante'
            else:
                item['result_type'] = 'normal'
            item['image_urls'] = result.select('.//div[@class="llg"]//img/@src').extract()
            self.position += 1
            item['position'] = self.position
            yield item

        for link in hxs.select('//a[@class="link_paginadoNew"]/@href').extract():
            yield Request(link, callback=self.parse)

        for link in hxs.select('//a[@class="link_paginadoNext"]/@href').extract():
            yield Request(link, callback=self.parse)

    def pop_or_nil(self, lst):
        if (len(lst) > 0):
            return lst.pop()
        else:
            return 0
