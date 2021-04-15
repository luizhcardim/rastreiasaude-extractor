# -*- coding: utf-8 -*-
import scrapy
from publichealth.items import PublichealthItem


class PrBemparanaSpider(scrapy.Spider):
    name = 'pr_bemparana'
    allowed_domains = ['www.bemparana.com.br']
    start_urls = ["https://www.bemparana.com.br/noticia/term/saude-e-beleza/"]

    def parse(self, response):

        # Abrindo cada uma das notícias
        for n in response.xpath('//section[@id="list-news"]//header'):
            link = n.xpath('./a/@href').get()
            yield response.follow(url=link, callback=self.parseNoticia)

        # Correndo pelas páginas de notícia
        for p in response.xpath('//li[@class="next"]/a/@href'):
            link = p.get()
            yield response.follow(url=link, callback=self.parse)


     # Parse das notícias 
    def parseNoticia(self, response):

        item = PublichealthItem()

        item['titulo'] = response.xpath('//div[@class="heading"]/h1/text()').get()
        item['conteudo'] = response.xpath('//div[@id="corpo"]//text()').getall()
        item['url'] = response.request.url

        # DATA

        d = response.xpath('//span[@class="published-date"]/@content').get()
        #d = d.split(' ')[0]

        item['data'] = d
    
        yield item
