# -*- coding: utf-8 -*-
import scrapy
from publichealth.items import PublichealthItem


class PrTribunaSpider(scrapy.Spider):
    name = 'pr_sesa'
    allowed_domains = ['www.saude.pr.gov.br']
    start_urls = ["http://www.saude.pr.gov.br/Noticias?combine=&field_editoria_target_id=All&published=1&published_range%5Bmin%5D=&published_range%5Bmax%5D=&sort_bef_combine=published_at%20DESC&sort_by=published_at&sort_order=DESC&page=1"]

    def parse(self, response):

        # Abrindo cada uma das notícias
        for n in response.xpath('//div[@class="list-noticias-page"]//h3'):
            link = n.xpath('./a/@href').get()
            yield response.follow(url=link, callback=self.parseNoticia)

        # Correndo pelas páginas de notícia
        for p in response.xpath('//li[@class="pager__item"]/a/@href'):
            link = p.get()
            yield response.follow(url=link, callback=self.parse)


     # Parse das notícias 
    def parseNoticia(self, response):

        item = PublichealthItem()

        item['titulo'] = response.xpath('//span[@id="story_title"]/span/text()').get()
        item['conteudo'] = response.xpath('//*[@id="content"]/div/div//text()').getall()
        item['url'] = response.request.url

        # DATA

        d = response.xpath('//*[@id="story_date"]/div/text()').get()
        item['data'] = d.split(' ')[0].strip()
        d = item['data'].split('/')
        item['data'] = d[2]+'-'+d[1]+'-'+d[0]

    
        yield item
