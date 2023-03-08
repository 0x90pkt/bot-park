from selenium import webdriver
import requests
from bs4 import BeautifulSoup


class shopper:
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(options=chrome_options)
        url = "https://www.costco.com/formula-feeding.html?brand=enfamil&refine=%7C%7CBrand_attr-Enfamil"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

    def check(self, url, headers):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        things = soup.findAll("img", {"alt": "Out of Stock"})
        print(things)

        atags = soup.findAll("a", {"class": "product-out-stock-overlay"})
        # print(atags)

        for tag in atags:
            search = "Out of Stock"
            mine = tag.find('')

            # if mine:
            #    temp = tag.text[:2] + mine['alt'] + tag.text[2:]
            #    if mine['alt'] == "Enfamil NeuroPro Care Gentlease Formula, 20 oz, 2-pack":
            #        found = mine
            #        print(temp)
            #        print(tag)
            #        print(tag.next_element.)
            # for i in found:
            #   stock = tag.
        # print(things)
