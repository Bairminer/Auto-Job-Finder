import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Search:
    def __init__(self, keywords, badwords):
        self.keywords = keywords
        self.badwords = badwords
        self.driver = webdriver.Safari()

    def get(self, link):
        self.driver.get(link)

    def search(self, keywords, badwords):
        weight = 0
        src = self.driver.page_source
        # add weight if match
        for i in keywords:
            if i.lower() in src:
                weight += 1
            else:
                if i.upper() in src:
                    weight += 1
        # auto reject
        for i in badwords:
            if i.lower() in src:
                return 0
            else:
                if i.upper() in src:
                    return 0

        return round(weight / len(keywords) * 100, 2)

    def scrape(self, page_link, sublink):
        self.get(page_link + "0")
        empty = False
        count = 0
        master_list = []
        while not empty and count < 1000: # max number of listings to save
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            # traverse list
            job_links = []
            for link in all_links:
                try:
                    url = link.get_attribute("href")
                    if sublink in url:
                        job_links.append(url)
                except:
                    continue
            #print(job_links)
            if len(job_links) == 0:
                return
            for link in job_links:
                try:
                    time.sleep(random.randint(0, 3)) # avoid bot detection
                    self.get(link)
                    score = self.search(self.keywords, self.badwords)
                    print(link, score, "%")
                    if score != 0:
                        master_list.append([link, score])
                except:
                    continue
            count += 10
            print(page_link + str(count))
            self.get(page_link + str(count))
        master_list.sort(key=lambda x: x[1])
        return master_list


    def __del__(self):
        self.driver.close()
