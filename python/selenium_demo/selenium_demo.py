#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: selenium_demo.py
@time: 2022-12-29
@desc: 
"""
import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from logutil import creater_logger

logger = creater_logger()


class Demo(object):
    def __init__(self, is_show=False):
        self.login_url = "http://1.1.1.1:1111/"
        self.token_verify_url = "http://2.2.2.2:2222/api/token/verify"
        self.username = "username"
        self.password = "password"
        self.driver_options = webdriver.ChromeOptions()
        if not is_show:
            self.driver_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=self.driver_options)

        self.token = ""

    def find_element_by_xpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            time.sleep(1)
            if element:
                return element
            else:
                return None
        except Exception as e:
            logger.exception(f"find_element by xpath error, xpath: {xpath}")
            return None

    def find_element_by_css_selector(self, css_selector):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            time.sleep(1)
            if element:
                return element
            else:
                return None
        except Exception as e:
            logger.exception(f"find_element by css_selector error, css_selector: {css_selector}")
            return None

    def login(self):
        logger.info(f"start login, url: {self.login_url}")
        self.driver.get(self.login_url)
        time.sleep(6)
        username_xpath = '//*[@id="username"]'
        password_xpath = '//*[@id="password"]/input'
        login_btn_xpath = '//*[@id="app"]/div/div/div[1]/div/div/div/div[2]/div[2]/div/form[2]/div[3]/div/div/span/button'
        user_elem = self.find_element_by_xpath(username_xpath)
        user_elem.clear()
        user_elem.send_keys(self.username)

        pwd_elem = self.find_element_by_xpath(password_xpath)
        pwd_elem.clear()
        pwd_elem.send_keys(self.password)

        btn_elem = self.find_element_by_xpath(login_btn_xpath)
        btn_elem.click()
        time.sleep(3)

        self.driver.refresh()
        time.sleep(10)
        for request in self.driver.requests:
            if request.url == self.token_verify_url:
                self.token = request.headers.get("Authorization")
                logger.info(f"token: {self.token}")
        self.driver.quit()


def main():
    demo = Demo(is_show=True)
    demo.login()


if __name__ == '__main__':
    main()
