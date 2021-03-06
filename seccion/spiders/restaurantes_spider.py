import re
import os
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
            item['full_url'] = self.pop_or_nil(result.select('.//a[@class="anclas"]/@href').extract())
            item['name'] = self.pop_or_nil(result.select('.//a[@class="anclas"]/text()').extract())
            if (not item['name']):
                item['name'] = self.pop_or_nil(result.select('.//td[1]/text()').extract())
            item['category'] = self.pop_or_nil(result.select('.//td[@class="categoria"]/a/text()').extract())
            item['address'] = self.pop_or_nil(result.select('.//tr[3]//strong/text()').extract())
            self.fill_address(item, item['address'])
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
            item['image_urls'] = self.pop_or_nil(result.select('.//div[@class="llg"]//img/@src').extract())
            self.position += 1
            item['position'] = self.position
            if (item['full_url']):
                request = Request(item['full_url'], callback=self.parse_restaurant)
                request.meta['item'] = item
                yield request
            else:
                yield item

        for link in hxs.select('//a[@class="link_paginadoNew"]/@href').extract():
            yield Request(link, callback=self.parse)

        for link in hxs.select('//a[@class="link_paginadoNext"]/@href').extract():
            yield Request(link, callback=self.parse)

    def parse_restaurant(self, response):
        hxs = HtmlXPathSelector(response)
        item = response.request.meta['item']

        for result in hxs.select('//span[@class="infoDireccionVentana"]/text()').extract():
            if ': ' in result.strip():
                values = result.strip().split(': ')
                if 'CORREO' in values[0]:
                    item['email'] = values[1]
                if 'GINA WEB' in values[0]:
                    item['homepage'] = values[1]

        item['horario'] = ''
        for result in hxs.select('//div[@id="textpwv"]//text()').extract():
            if len(result.strip()) == 0:
                continue
            if "Horario" in result.strip():
                continue
            if "Formas de pago" in result.strip():
                continue

            if len(item['horario']):
                if re.search('\w', item['horario'][-1]):
                    item['horario'] += " "
                else:
                    item['horario'] += "\n"

            item['horario'] += result.strip()

        item['formas_de_pago'] = []
        for result in hxs.select('//div[@class="recuadroFormasPago"]//table//img/@src').extract():
            item['formas_de_pago'].append( os.path.split(result)[1].split('.')[0] )
        item['formas_de_pago'] = ", ".join( item['formas_de_pago'] )

        for result in hxs.select('//h4[@class="categoria"]'):
            cat, content = result.select('.//text()').extract()
            if 'SERVICIOS' in cat:
                item['servicios'] = content
            elif 'MARCAS' in cat:
                item['marcas'] = content
            elif 'INFORMACION' in cat:
                item['informacion'] = content

        yield item

    def pop_or_nil(self, lst):
        if (len(lst) > 0):
            return lst[0]
        else:
            return ''

    def fill_address(self, item, address):
        if (address != 0):
            address = [x.strip() for x in address.split("\r\n")]
            item['street'] = address[0]
            item['colony'] = '' if (len(address) < 2) else address[2]
            item['zipcode'] = '' if (len(address) < 4) else address[4]
            item['city'] = '' if (len(address) < 6) else address[6]
            if (item['city'] == u'JAL'):
                item['state'] = u'JAL'
                item['city'] = ''
            item['state'] = '' if (len(address) < 8) else address[8]
