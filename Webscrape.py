import csv
from bs4 import BeautifulSoup 
from selenium import webdriver
import json
import numpy as np
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

MAX = 10000000


#url = 'https://www.amazon.com'


def getUrl(search):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search = search.replace(' ', '+')
    return template.format(search)

def cheapest(item):
    firstmin = MAX
    secmin = MAX
    thirdmin = MAX

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
                return record[2]
                newAmount = filter(str.isdigit, record[2])
                finalAmount = "".join(newAmount)
                newPrice.append(finalAmount)
            records.append(record)

    records = np.array(records)
    newPrice = np.array(newPrice)
    print(newPrice)

    res1 = 0
    res2 = 0
    res3 = 0
    name = item
    

    #minimum = min(newPrice)

    #print(minimum)
    if len(newPrice) > 0:
        for i in range(len(newPrice)):
          
        # Check if current element
        # is less than firstmin, 
        # then update first,second
        # and third
  
            if float(newPrice[i]) < float(firstmin):
                thirdmin = secmin
                secmin = firstmin
                firstmin = newPrice[i]
    
            # Check if current element is
            # less than secmin then update
            # second and third
            elif float(newPrice[i]) < float(secmin):
                thirdmin = secmin
                secmin = newPrice[i]
    
            # Check if current element is
            # less than,then upadte third
            elif float(newPrice[i]) < float(thirdmin):
                thirdmin = newPrice[i]
        
        ret = []
        ret.append(firstmin)
        ret.append(secmin)
        ret.append(thirdmin)
        return ret

        for i in range(records.shape[0]):
            records[i][3] = records[i][3].replace('$', '')
            if float(records[i][3]) == float(firstmin):
                iteration1 = i
            elif float(records[i][3]) == float(secmin):
                iteration2 = i
            elif float(records[i][3]) == float(thirdmin):
                iteration3 = i
            else:
                iteration1 = 0
                iteration2 = 0
                iteration3 = 0


        final1 = records[iteration1]
        final2 = records[iteration2]
        final3 = records[iteration3]
        if "ounce" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("ounce")[0]
            res1 = res1.split()[-1]

        elif "pounds" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("pounds")[0]
            res1 = res1.split()[-1]
            res1 = float(res1) * 16
        elif "lbs" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("lbs")[0]
            res1 = res1.split()[-1]
            res1 = float(res1) * 16
        elif "lb" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("lb")[0]
            res1 = res1.split()[-1]
            res1 = float(res1) * 16
        elif "fl" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("fl")[0]
            res1 = res1.split()[-1]
        elif "oz" in records[iteration1][4].lower():
            res1 = records[iteration1][4].lower().split("oz")[0]
            res1 = res1.split()[-1]

        
        if "ounce" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("ounce")[0]
            res2 = res2.split()[-1]

        elif "pounds" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("pounds")[0]
            res2 = res2.split()[-1]
            res2 = float(res2) * 16
        elif "lbs" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("lbs")[0]
            res2 = res2.split()[-1]
            res2 = float(res2) * 16
        elif "lb" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("lb")[0]
            res2 = res2.split()[-1]
            res2 = float(res2) * 16
        elif "fl" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("fl")[0]
            res2 = res2.split()[-1]
        elif "oz" in records[iteration2][4].lower():
            res2 = records[iteration2][4].lower().split("oz")[0]
            res2 = res2.split()[-1]


        if "ounce" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("ounce")[0]
            res3 = res3.split()[-1]

        elif "pounds" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("pounds")[0]
            res3 = res3.split()[-1]
            res3 = float(res3) * 16
        elif "lbs" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("lbs")[0]
            res3 = res3.split()[-1]
            res3 = float(res3) * 16
        elif "lb" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("lb")[0]
            res3 = res3.split()[-1]
            res3 = float(res3) * 16
        elif "fl" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("fl")[0]
            res3 = res3.split()[-1]
        elif "oz" in records[iteration3][4].lower():
            res3 = records[iteration3][4].lower().split("oz")[0]
            res3 = res3.split()[-1]

        subItem1 = {
            "Rating": final1[0],
            "Count": final1[1],
            "Amount": final1[2],
            "Total": res1,
            "price": final1[3],
            "description": final1[4],
            "url": final1[5]
        }
        subItem2 = {
            "Rating": final2[0],
            "Count": final2[1],
            "Amount": final2[2],
            "Total": res2,
            "price": final2[3],
            "description": final2[4],
            "url": final2[5]
        }
        subItem3 = {
            "Rating": final3[0],
            "Count": final3[1],
            "Amount": final3[2],
            "Total": res3,
            "price": final3[3],
            "description": final3[4],
            "url": final3[5]
        }
    else:
        for i in range(len(records)):
          
            # Check if current element
            # is less than firstmin, 
            # then update first,second
            # and third
            records[i][3] = records[i][3].replace('$', '')
            if float(records[i][3]) < firstmin:
                thirdmin = secmin
                secmin = firstmin
                firstmin = records[i][3]
    
            # Check if current element is
            # less than secmin then update
            # second and third
            elif records[i][3] < secmin:
                thirdmin = secmin
                secmin = records[i][3]
    
            # Check if current element is
            # less than,then upadte third
            elif records[i][3] < thirdmin:
                thirdmin = records[i][3]
            
            for i in range(len(records)):
                if records[i][3] == float(firstmin):
                    iteration1 = i
                    final1 = records[i]
                elif records[i][3] == float(secmin):
                    iteration2 = i
                    final2 = records[i]
                elif records[i][3] == float(thirdmin):
                    iteration3 = i
                    final3 = records[i]
            
            subItem1 = {
            "Rating": final1[0],
            "Count": final1[1],
            "Amount": final1[2],
            "price": final1[3],
            "description": final1[4],
            "url": final1[5]
        }
        subItem2 = {
            "Rating": final2[0],
            "Count": final2[1],
            "Amount": final2[2],
            "price": final2[3],
            "description": final2[4],
            "url": final2[5]
        }
        subItem3 = {
            "Rating": final3[0],
            "Count": final3[1],
            "Amount": final3[2],
            "price": final3[3],
            "description": final3[4],
            "url": final3[5]
        }



    items = []
    items.append(subItem1)
    items.append(subItem2)
    items.append(subItem3)

    
    return items

    #print(res)
    #print(final)


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

app = Flask(__name__)
api = Api(app)
CORS(app)

class Web(Resource):
    def get(self, name):
        return cheapest(name)
api.add_resource(Web, "/subItem/<string:name>")
        
if __name__ == "__main__":
    app.run(debug=True)

#cheapest('Sugar')
#cheapest('Syrup')