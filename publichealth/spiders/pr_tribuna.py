# -*- coding: utf-8 -*-
import scrapy
from publichealth.items import PublichealthItem


class PrTribunaSpider(scrapy.Spider):
    name = 'pr_tribuna'
    allowed_domains = ['www.tribunapr.com.br']
    start_urls = ["https://www.tribunapr.com.br/noticias/parana/","https://www.tribunapr.com.br/noticias/curitiba-regiao/"]

    def parse(self, response):

        # Abrindo cada uma das notícias
        for n in response.xpath('//section[@class="post-list"]/article'):
            link = n.xpath('.//a/@href').get()
            yield response.follow(url=link, callback=self.parseNoticia)

        # Correndo pelas páginas de notícia
        for p in response.xpath('//div[@class="pagination__lazyload pagination"]//a/@href'):
            link = p.get()
            yield response.follow(url=link, callback=self.parse)


     # Parse das notícias 
    def parseNoticia(self, response):

        item = PublichealthItem()

        item['titulo'] = response.xpath('//h1[contains(@class, "post-title") or contains(@class, "post-title ")]/text()').get()
        item['conteudo'] = response.xpath('//section[@id="post-content"]//p//text()').getall()
        item['url'] = response.request.url

        # DATA

        d = response.xpath('//time/@datetime').get()
        d = d.split(' ')[0]

        item['data'] = d
    
        yield item
