import scrapy
import pandas as pd

import re
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from articlescrapper.items import ArticlescrapperItem

input = pd.read_excel(r'C:\Users\bherw\OneDrive\Desktop\Suraj\Test\Blackcoffer\articlescrapper\articlescrapper\spiders\Input.xlsx')
# urls = input['URL'].to_numpy()
# uids = input['URL_ID']

class ArticlespiderSpider(scrapy.Spider):
    urls = input['URL'].to_numpy()
    uids = input['URL_ID']
    id = 0
    name = "articlespider"
    allowed_domains = ["insights.blackcoffer.com"]
    # start_urls = [url for url in urls]


    #['https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/']#["https://insights.blackcoffer.com"]

    # def start_requests(self):
    #     urls = "https://insights.blackcoffer.com/rise-of-cyber-crime-and-its-effects/"
    #     yield scrapy.Request(urls, meta=dict(
    #         playwright = True,
    #         playwright_include_page = True,
    #         playwright_page_methods = [
    #             PageMethod('wait_for_selector', 'div.td-post-content'),
    #         ],
    #     ))

    def start_requests(self):
        for url in self.urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'td-post-content')))

    def parse(self, response):
        articleItem = ArticlescrapperItem()

        articleItem['uid'] = self.uids[self.id]
        articleItem['title'] = response.css('h1').get()
        articleItem['article'] = response.css('div.td-post-content').get()

        # print(self.uids[self.id] + "--------------------------------------------------------")

        # file = open(f"articles/{uids[id]}", 'w')
        file = open(f"articles/{articleItem['uid']}.txt", 'w+', encoding="utf-8")
        file.write(articleItem['title'] + " " + articleItem['article'])
        file.close()
        self.id += 1

        yield articleItem



