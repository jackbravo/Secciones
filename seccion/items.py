# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RestauranteItem(Item):
    name = Field()
    picture = Field()
    address = Field()
    street = Field()
    colony = Field()
    zipcode = Field()
    city = Field()
    state = Field()
    phone = Field()
    category = Field()
    rating = Field()
    num_reviews = Field()
    full_url = Field()
    position = Field()
    result_type = Field() # contlist, result_Diamante, result
    image_urls = Field()
    images = Field()
    pass
