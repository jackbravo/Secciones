# Scrapy settings for seccion project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'seccion'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['seccion.spiders']
NEWSPIDER_MODULE = 'seccion.spiders'
DEFAULT_ITEM_CLASS = 'seccion.items.RestauranteItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
#ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
#IMAGES_STORE = 'images'

