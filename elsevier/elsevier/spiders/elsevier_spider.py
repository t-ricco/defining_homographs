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
            '//*[@id="introduction"]/table/tbody/tr[2]/td[1]/a/@href'
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
            '//*[@id="LeftCol1"]/div[1]/a/@href'
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
        url_start = url.split('/')[0]

        for href in response.xpath(
            # '//div[@id="search-container"]/ol/li/article/div/h3/a/@href'
            #'//h3[@class="ResultsList_title"]/a/@href'
            '//*[@id="latest-published-articles"]/div/div/a/@href'
        ).extract():

            cutoff = href.find('pdf')
            href = url_start + href[:cutoff]

            #print('**********************************\n\nparse_journal_list: ',href,"\n\n#")

            yield scrapy.Request(
                url=href,
                callback=self.parse_journal,
                meta={'url': href}
            )

    def parse_article(self, response):

        items = ElsevierItem()

        url = response.request.meta['url']
        title = response.xpath('//*[@class="article-title"]/span/text()').extract()
        authors_given_names = response.xpath('//*[@class="text given-name"]/text()').extract()
        authors_surnames = response.xpath('//*[@class="text surname"]/text()').extract()
        publication = response.xpath('//*[@class="publication-title-link"]/text()').extract()
        publication_date = response.xpath('//*[@class="publication-volume"]/div/span/text()').extract()[1]
        abstract = response.xpath('//*[@class="Abstracts"]/div/div/p/text()').extract()[0]

        full_text = ''.join(response.xpath('//*[@id="react-root"]/div/div/div/div/section/div/div[2]/div[2]/article/div/text()').extract())

        authors = [' '.join(x) for x in zip(authors_given_names, authors_surnames)]
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
        items['publication_date'] = publication_date
        items['abstract'] = abstract
        items['full_text'] = full_text

        #print(items, "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        yield items

    def errback_storage(self, failure):
        yield failure.value