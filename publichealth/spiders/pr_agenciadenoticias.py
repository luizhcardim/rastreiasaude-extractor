# -*- coding: utf-8 -*-
import scrapy
from publichealth.items import PublichealthItem


class PrAgencianoticiasSpider(scrapy.Spider):
    name = 'pr_agencianoticias'
    allowed_domains = ['www.aen.pr.gov.br']
    start_urls = ["http://www.aen.pr.gov.br/modules/noticias/ajaxResults.php?order=DESC&start=0&topic_id=53&strsearch=&publish_start=&publish_end=&regiao=0"]

    

    def parse(self, response):

        page = 1

        # Abrindo cada uma das notícias
        for n in response.xpath('//ul[@class="lista"]//li'):
            link = n.xpath('./a/@href').get()
            yield response.follow(url=link, callback=self.parseNoticia)

        # Correndo pelas páginas de notícia
        for p in range(102):
            link = "http://www.aen.pr.gov.br/modules/noticias/ajaxResults.php?order=DESC&start="+str(p*30)+"&topic_id=53&strsearch=&publish_start=&publish_end=&regiao=0"
            yield response.follow(url=link, callback=self.parse)


     # Parse das notícias 
    def parseNoticia(self, response):

        item = PublichealthItem()

        item['titulo'] = response.xpath('//h1/text()').get()
        item['conteudo'] = response.xpath('//article[@class="content"]//text()').getall()
        item['url'] = response.request.url

        # DATA

        d = response.xpath('//*[@id="mp-pusher"]/div/div[1]/section/div[2]/div/div/div[1]/aside/dl/dd[1]/p/text()').get()
        d = d.split(' ')[0].strip()
        d = d.split('/')
        item['data'] = d[2]+'-'+d[1]+'-'+d[0]

    
        yield item
