# basic structure based on https://youtu.be/VJ8d9GSB2rw?t=445

import scrapy
from ..items import ScrapyLoginItem
from scrapy.shell import inspect_response
from scrapy.shell import open_in_browser
from scrapy.statscollectors import StatsCollector


class AgnesMonitor(scrapy.Spider):
    name = 'agnes-monitor'
    start_urls = ['https://agnes.hu-berlin.de/lupo/rds?state=wlogin&login=in&breadCrumbSource=portal']

    def start_requests(self):
        """starts login on agnes.hu-berlin.de - first try"""
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url,
                                     callback=self.second_request,
                                     formdata={'username': 'INSERT YOUR AGNES USERNAME HERE',
                                               'password': 'INSERT YOUR AGNES PASSWORD HERE',
                                               'login': ' Login '})

    def open_browser(self, response):
        open_in_browser(response)

    def second_request(self, response):
        """login on agnes.hu-berlin.de - second try"""
        yield scrapy.FormRequest.from_response(response,
                                               callback=self.third_request,
                                               formdata={'username': 'INSERT YOUR AGNES USERNAME HERE',
                                                         'password': 'INSERT YOUR AGNES PASSWORD HERE',
                                                         'login': ' Login '})

    def third_request(self, response):
        """login on agnes.hu-berlin.de - third and last try"""
        yield scrapy.FormRequest.from_response(response,
                                               callback=self.logged_in,
                                               formdata={'username': 'INSERT YOUR AGNES USERNAME HERE',
                                                         'password': 'INSERT YOUR AGNES PASSWORD HERE',
                                                         'login': ' Login '},
                                               dont_filter=True)

    def logged_in(self, response):
        """prints name of user if successfully logged into account on agnes.hu-berlin.de"""
        clean_name = response.css('.hu_loginInfoLinie .hu_loginlinks::text').re('\S+')
        print('\n'*2)
        for i in clean_name:
            print(i, end=' ') # prints name of user to verify success of login
        print('\n'*2)
        yield scrapy.http.Request(
            url='https://agnes.hu-berlin.de/lupo/rds?state=user&type=0&breadCrumbSource=&topitem=functions',
            callback=self.get_target_url)

    def get_target_url(self, response):
        """finding and accessing transcript of records URL"""
        target_url = response.css(':nth-child(10) .auflistung::attr(href)').extract_first()
        yield scrapy.http.Request(url=target_url,
                                  callback=self.verify_transcript)

    def verify_transcript(self, response):
        """verifying that you accessed the Transcript Of Records URL - prints the Header or ERROR"""
        if 'Trancript Of Records' in response.text:
            print('\n'*2)
            print('FOUND ' + response.css('h1::text').extract_first()) # prints 'FOUND Transcript of Records' if possible to access Transcript of Records URL
            print('\n'*2)
            yield scrapy.http.Request(url=response.url,
                                      callback=self.count_results,
                                      dont_filter=True)
        else:
            print('\n'*2)
            print('ERROR: got no Transcript of Records...')
            print('\n'*2)

    def count_results(self, response):
        """printing the number of lines in your Transcript Of Records table"""
        result_css = response.css('.lspiegel.lspiegelBottomBorder:not(.lspiegelLeftBorder):not(.lspiegelRightBorder)::text')
        print('\n'*2)
        result_amount = len(result_css)
        print('You got this many lines in your Transcript of Records: ' + str(result_amount)) # printing the number of lines in your Transcript Of Records table
        print('\n'*2)

        for line in result_css:
            yield {'Exam name': line.get()} # collecting the Exam names listed in your Transcript of Records table
