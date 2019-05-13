# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:03:29 2019

@author: sherl
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

def createBrowser(path):
    caps = DesiredCapabilities.CHROME    
    browser = webdriver.Chrome(desired_capabilities=caps, executable_path=path)
    browser.set_page_load_timeout(20)
    
    return browser

def extractTimeTable(url,browser):
    try:
        content = requests.get(url)
    except TimeoutException:
        browser.execute_script('window.stop()')
        
    soup = BeautifulSoup(content.text, "html.parser")
    tables = soup.findAll('table')
    tr = tables[41].findAll('tr')
    time_table = []
    row = []
    for ix,td in enumerate(tr):
        tds = td.findAll('td')
        if ix == 0:
            title = []
            for td in tds:
                title.append(td.get_text())
        else:
            row = []
            for td in tds:
                row.append(td.get_text())
            time_table.append(row)
    res = pd.DataFrame(time_table,columns=title)
    return res

def searchTimeTable(browser, cities:list):
    browser.get('http://www.gaotie.cn/')
    home_handle = browser.current_window_handle
    
    for city in cities:
        try:
            search_bar = browser.find_element_by_id('txtchezhan')
            search_bar.clear()
            browser.find_element_by_id('txtchezhan').send_keys(city)
            try:
                browser.find_element_by_xpath(
                    '//*[@id="box"]/div[2]/div[1]/table/tbody/tr/td[11]/input'
                    ).click()
            except TimeoutException:
                browser.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
        except:
            continue
        
        all_window_handle = browser.window_handles
        
        browser.switch_to.window(all_window_handle[-1])
        browser.set_page_load_timeout(20)
        try:
            browser.find_element_by_xpath(
                '/html/body/div[3]/div/table[2]/tbody/tr/td/a[2]'
                ).click()
        except TimeoutException:
             browser.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
        url = browser.current_url
        
        rlt = extractTimeTable(url,browser)
        rlt.to_csv('{}.csv'.format(city),index=False,encoding='utf_8_sig')

        browser.close()
        browser.switch_to.window(home_handle)
    browser.close()
    
if __name__ == '__main__':
    browser = createBrowser('chromedriver.exe')
    searchTimeTable(browser,['宁波','绍兴','汉口'])

    
