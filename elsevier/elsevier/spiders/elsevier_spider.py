# -*- coding: utf-8 -*-
import scrapy
import re
from elsevier.items import ElsevierItem


class ElsevierSpider(scrapy.Spider):
    name = 'elsevier_spider'
    #allowed_domains = ['www.springeropen.com','appliednetsci.springeropen.com']
    start_urls = ['https://www.elsevier.com/about/open-science/open-access/open-access-journals']

    def parse(self, response):
        
        for href in response.xpath(
            '//*[@id="introduction"]/table/tbody/tr[2]/td[1]/a'
        ).extract():

            yield scrapy.Request(
                url=href,
                callback=self.go_to_articles,
                errback=self.errback_storage,
                meta={'url': href}
            )


    def go_to_articles(self, response):

        url = response.request.meta['url']

        #print("!!!!!!!!!!!!!!!!!!!!\n\n",url,"\n\n!!!!!!!!!!!!!!!!!!!")

        for href in response.xpath(
            # '//div[@id="search-container"]/ol/li/article/div/h3/a/@href'
            #'//h3[@class="ResultsList_title"]/a/@href'
            '//*[@id="LeftCol1"]/div[1]/a'
        ).extract():

            #print('**********************************\n\nparse_journal_list: ',href,"\n\n#")

            yield scrapy.Request(
                url=href,
                callback=self.parse_journal,
                meta={'url': href}
            )

        
    def parse_journal(self, response):

        url = response.request.meta['url']

        #print("!!!!!!!!!!!!!!!!!!!!\n\n",url,"\n\n!!!!!!!!!!!!!!!!!!!")

        for href in response.xpath(
            # '//div[@id="search-container"]/ol/li/article/div/h3/a/@href'
            #'//h3[@class="ResultsList_title"]/a/@href'
            '//*[@id="latest-published-articles"]/div/div/a/@href'
        ).extract():

            #print('**********************************\n\nparse_journal_list: ',href,"\n\n#")

            yield scrapy.Request(
                url=href,
                callback=self.parse_journal,
                meta={'url': href}
            )

    def parse_article(self, response):

        items = ElsevierItem()

        url = response.request.meta['url']
        title = response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/div[2]/h1/span/text()').extract()[0]
        authors = response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/div[3]/div/div/div/text()').extract()
        publication = response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/div[1]/div[2]/h2/span/a/text()').extract()[0]
        publication_date = response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/div[1]/div[2]/div/span/text()[2]').extract()[0].split('\xa0')
        abstract = response.xpath('//*[@id="sp0035"]/text()').extract()
        full_text = ''.join(response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/article/div/text()').extract())

        #authors = [''.join([y + ' ' for y in x.split('\xa0')]).strip() for x in authors]
        #if len(abstract) > 0:
        #    abstract = abstract[0]

        #print('$$$$$$$$$$$$$$$$\n\nfinished: ',title,'\n',
        #    url,'\n',
        #    authors,'\n',
        #    publication,'\n',
        #    publication_date,'\n',
        #    abstract[:20],'\n',
        #    full_text[:20],'\n',
        #    '$$$$$$$$$$$$$$')

        items['url'] = url
        items['title'] = title
        items['authors'] = authors
        items['publication'] = publication
        items['publication_date'] = ''.join([x+' ' for x in publication_date]).strip()
        items['abstract'] = abstract
        items['full_text'] =  full_text

        #print(items, "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        yield items

    def errback_storage(self, failure):
        yield failure.value