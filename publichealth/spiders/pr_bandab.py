# -*- coding: utf-8 -*-
import scrapy
from publichealth.items import PublichealthItem


class PrBandabSpider(scrapy.Spider):
    name = 'pr_bandab'
    allowed_domains = ['www.bandab.com.br']
    start_urls = ["https://www.bandab.com.br/noticias/categoria/saude/"]

    def parse(self, response):

        # Abrindo cada uma das notícias
        for n in response.xpath('//div[@class="infinite"]//div[@class="module module-news-5"]'):
            link = n.xpath('./a/@href').get()
            yield response.follow(url=link, callback=self.parseNoticia)

        # Correndo pelas páginas de notícia
        for p in response.xpath('//ul[@class="page-numbers"]//a[@class="next page-numbers"]/@href'):
            link = p.get()
            yield response.follow(url=link, callback=self.parse)


     # Parse das notícias 
    def parseNoticia(self, response):

        item = PublichealthItem()

        item['titulo'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['conteudo'] = response.xpath('//div[@class="post-content"]//text()').getall()
        item['url'] = response.request.url

        # DATA

        d = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        

        item['data'] = d
    
        yield item
