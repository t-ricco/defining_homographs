# -*- coding: utf-8 -*-
import scrapy
import re
from abstract_scraper.items import AbstractScraperItem


class AbstractSpiderSpider(scrapy.Spider):
    name = 'abstract_spider'
    #allowed_domains = ['www.springeropen.com','appliednetsci.springeropen.com']
    start_urls = ['http://www.springeropen.com/journals-a-z']

    def parse(self, response):
        
        for href in response.xpath(
            '//div[@id="journalList"]/ol[2]/li/ol/li/a/@href'
        ).extract():

            href = 'https:' + href + "/articles"

            yield scrapy.Request(
                url=href,
                callback=self.parse_journal_list,
                errback=self.errback_storage,
                meta={'url': href}
            )

        
    def parse_journal_list(self, response):

        url = response.request.meta['url']

        #print("!!!!!!!!!!!!!!!!!!!!\n\n",url,"\n\n!!!!!!!!!!!!!!!!!!!")

        for href in response.xpath(
            # '//div[@id="search-container"]/ol/li/article/div/h3/a/@href'
            '//h3[@class="ResultsList_title"]/a/@href'
        ).extract():

            url = re.sub('/articles', '', url)
            href = url + href
            #print('**********************************\n\nparse_journal_list: ',href,"\n\n#")

            yield scrapy.Request(
                url=href,
                callback=self.parse_journal,
                meta={'url': href}
            )

        # next_url = url + response.xpath('//*[@id="search-container"]/div[2]/div/a/@href').extract()[0]
        next_url = url + response.xpath('//a[@class="Pager Pager--next"]/@href').extract_first()

        yield scrapy.Request(
            url=next_url,
            callback=self.parse_journal_list
        )

    def parse_journal(self, response):

        items = AbstractScraperItem()

        url = response.request.meta['url']
        title = response.xpath('//*[@id="Test-ImgSrc"]/div[2]/div[1]/h1/text()').extract()[0]
        authors = response.xpath('//*[@id="Test-ImgSrc"]/div[2]/div[2]/ul/li/span/text()').extract()
        publication = response.xpath('//*[@id="Test-ImgSrc"]/div[2]/div[3]/div/div/span/span[1]/text()').extract()[0]
        publication_date = response.xpath('//*[@id="Test-ImgSrc"]/div[2]/div[4]/p[3]/text()').extract()[0].split('\xa0')
        abstract = response.xpath('//*[@id="Abs1"]/div/div/p/text()').extract()
        full_text = ''.join(response.xpath('//*[@class="FulltextWrapper"]/section/div/p/text()').extract())

        authors = [''.join([y + ' ' for y in x.split('\xa0')]).strip() for x in authors]
        if len(abstract) > 0:
            abstract = abstract[0]

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