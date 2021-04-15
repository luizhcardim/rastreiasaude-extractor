# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PublichealthItem(scrapy.Item):
    # define the fields for your item here like:
    cidades = scrapy.Field()
    titulo = scrapy.Field()
    data = scrapy.Field() # Fazer método para tratar
    conteudo = scrapy.Field()
    url = scrapy.Field()
    project = scrapy.Field()
    doencas = scrapy.Field()
    tipo = scrapy.Field()



