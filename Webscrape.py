import csv
from bs4 import BeautifulSoup 
from selenium import webdriver
import re
import numpy as np



#url = 'https://www.amazon.com'


def getUrl(search):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search = search.replace(' ', '+')
    return template.format(search)

def cheapest(item):
    driver = webdriver.Chrome()
    url = getUrl(item)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result = soup.find_all('div', {'data-component-type': 's-search-result'})

    records = []
    newPrice = []
    for item in result:
        record = extract_record(item)
        if record:
            if "Ounce" in record[2] or "Oz" in record[2]:
                newAmount = filter(str.isdigit, record[2])
                finalAmount = "".join(newAmount)
                records.append(record)
                newPrice.append(finalAmount)


    newPrice = np.array(newPrice)
    print(newPrice)

    minimum = min(newPrice)

    #print(minimum)

    for i in range(len(records)):
        if newPrice[i] == minimum:
            iteration = i

    final = records[iteration]
    if "ounce" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("ounce")[0]
        res = res.split()[-1]

    elif "pounds" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("pounds")[0]
        res = res.split()[-1]
        res = int(res) * 16
    elif "lbs" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("lbs")[0]
        res = res.split()[-1]
        res = int(res) * 16
    elif "lb" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("lb")[0]
        res = res.split()[-1]
        res = int(res) * 16
    elif "fl" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("fl")[0]
        res = res.split()[-1]
    elif "oz" in records[iteration][4].lower():
        res = records[iteration][4].lower().split("oz")[0]
        res = res.split()[-1]


    print(res)
    print(final)


    #print(final)


def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    
    except AttributeError:
        return

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text

    except AttributeError:
        rating = ''
        review_count = ''

    try: 
        amount = item.find('span', {'class': 'a-size-base a-color-secondary', 'dir': 'auto'}).text
    except AttributeError:
        amount = ''

    result = (rating, review_count, amount, price, description, url)

    return result




#cheapest('Sugar')
cheapest('Syrup')