import scrapy
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class PhonesPrices(scrapy.Spider):
    name = "phones_prices"
    start_urls = ['https://comfy.ua/smartfon/']


    def __init__(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("intl.accept_languages", "ua_RU")
        self.profile.set_preference("dom.disable_open_during_load", False)
        # self.profile.set_preference("general.useragent.override", "[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36]")
        self.fireFoxOptions = webdriver.FirefoxOptions()
        self.fireFoxOptions.set_headless()
        self.driver = webdriver.Firefox(firefox_profile=self.profile, firefox_options=self.fireFoxOptions)


    def parse(self, response):
        resp = self.driver.get(response.url)
        for _ in range(6):
            sleep(12)
            response = Selector(text=self.driver.page_source)
            try:
                pop_up = self.driver.find_element_by_css_selector(".popup-close")
                pop_up.click()
            except:
                pass

            for data in response.css('div.product-item__i'):
                price = data.css('div.price-box__content-i .price-value::text').get()
                yield {
                        'Text': data.css('div > p > a::attr(title)').get(),
                        'Link': data.css('div.product-item__i > p > a::attr(href)').get(),
                        'Price': price.strip()
                }
            sleep(19)
            scroll_next = self.driver.find_element_by_css_selector(".category-pager")
            self.driver.execute_script("arguments[0].scrollIntoView();", scroll_next)
            sleep(9)
            next_page = self.driver.find_element_by_css_selector(".category-pager > div:nth-child(1) > div:nth-child(3) > ul:nth-child(1) > li:nth-child(7) > a:nth-child(1)")
            next_page.click()
            sleep(25)
            response = Selector(text=self.driver.page_source)
            sleep(5)

        self.driver.close()
