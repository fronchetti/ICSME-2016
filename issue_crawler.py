#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luiz Felipe Fronchetti
# Special thanks to Luiz H. Susin, who collaborated with a similar code in Java.

import scrapy
import os
import json
from datetime import datetime

class IssueSpider(scrapy.Spider):
    """
    Spiders are classes which define how a certain site (or a group of sites) will be scraped, including how to perform the crawl (i.e. follow links) 
    and how to extract structured data from their pages (i.e. scraping items). In other words, Spiders are the place where you define the custom behaviour 
    for crawling and parsing pages for a particular site (or, in some cases, a group of sites).

        How to use:
                to collect Rails project issues (page one to ten), via terminal, use:
                    $ scrapy runspider IssueSpider.py -a filename=rails.txt -a url=https://github.com/rails/rails -a firstpage=1 -a lastpage=10

        Variables:
                name: A string which defines the name for this spider.
                allowed_domains: An optional list of strings containing domains that this spider is allowed to crawl.
                start_urls: A list of URLs where the spider will begin to crawl from.
                custom_settings: A dictionary of settings that will be overridden from the project wide configuration when running this spider. 

        Methods:
                __init__: initial method, receives parameters by reference and instantiates the utility class .
                parse: default callback used by Scrapy to process downloaded responses, returns the url of each issue available on the issues table [1].
                parse_inside_issue: in this method we extract all data, issue by issue [2].
                
        [1] Issues Table Page Example: https://github.com/rails/rails/issues
        [2] Issue Page Example: https://github.com/rails/rails/issues/1
        * Read more about Scrapy Spiders at: http://doc.scrapy.org/en/latest/topics/spiders.html 
    """

    name = 'IssueSpider'
    allowed_domains = ['github.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 1,
        'COOKIES_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def __init__(self, filename=None, url=None, firstpage=None, lastpage=None, *args, **kwargs):
        super(IssueSpider, self).__init__(*args, **kwargs)
        self.utils = Utils(filename)
        self.utils.write_header()
        self.start_urls = self.utils.define_start_urls(url, firstpage, lastpage)

    def parse(self, response):
        for sel in response.xpath('//li//div[@class="d-table width-full Box-row--drag-hide lh-condensed"]//div[@class="d-table-cell width-full p-3"]'):
            url = sel.xpath('a/@href').extract()[0]
            url = ('https://github.com' + url)
            yield scrapy.Request(url, callback=self.parse_inside_issue)

    def parse_inside_issue(self, response):
        for sel in response.xpath('//div[@class="issues-listing"]'):
            number = sel.xpath('//div[@class="gh-header-show "]//span[@class="gh-header-number"]/text()').extract()
            header = sel.xpath('//div[@class="flex-table gh-header-meta"]//div[@class="flex-table-item flex-table-item-primary"]')
            comment = header.xpath('text()').extract()
            author = header.xpath('a[@class="author"]/text()').extract()
            open_date = header.xpath('relative-time/@datetime').extract()
        close_date = response.xpath('//div[@class="discussion-item discussion-item-closed"]//div[@class="discussion-item-header"]//relative-time[@class="timestamp"]/@datetime').extract()
        tags = response.xpath('//span[@class="timeline-comment-label"]/text()').extract()
        self.utils.write_issue(number, comment, author, open_date, close_date, tags)


class Utils():

    def __init__(self, file_name):
        self.file_destination = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name

    def define_start_urls(self, url, firstpage, lastpage):
        start_urls = []
        for page_number in range(int(firstpage), int(lastpage)):
            start_urls.append(url + '/issues?page=' + str(page_number) + '&q=is%3Aissue')
        return start_urls

    def write_header(self):
        header_data = 'Identifier, Author, Author Tag, Number of Comments, Opening Date, Closing Date \n'

        with open(self.file_destination, 'w') as f:
            f.write(header_data)
            f.close()

    def write_issue(self, number, comment, author, open_date, close_date, tags):
        number = number[0].encode('utf-8').strip()
        author = author[0].encode('utf-8').strip()
        comment = comment[3].encode('utf-8').strip()

        open_time_string = datetime.strptime(open_date[0], '%Y-%m-%dT%H:%M:%SZ')
        open_date_format = open_time_string.strftime('%d/%m/%Y').encode('utf-8')

        if not close_date:
            close_date_format = 'None'
        else:
			if len(close_date) > 1:	
				close_date_format = None
				for date in close_date:
					close_time_string = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
					if not close_date_format:
						close_date_format = close_time_string.strftime('%d/%m/%Y').encode('utf-8')
					else:
						close_date_format = close_date_format + ' - ' + close_time_string.strftime('%d/%m/%Y').encode('utf-8')
			else:
					close_time_string = datetime.strptime(close_date[0], '%Y-%m-%dT%H:%M:%SZ')
					close_date_format = close_time_string.strftime('%d/%m/%Y').encode('utf-8')
				
        if not tags:
            tags_format = 'None'
        else:
            tags_format = []
            for tag in tags:
                if tag not in tags_format:
                    tags_format.append(tag.encode('utf-8').strip())
        
        
        with open(self.file_destination, 'a') as f:
            f.write(
            number + ', ' + author + ', ' + str(tags_format) + ', ' + 
            comment + ', ' + str(open_date_format) + ', ' + str(close_date_format) + '\n')
            f.close()
