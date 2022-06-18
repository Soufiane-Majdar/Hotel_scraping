from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from lxml import etree
import requests
  
  

##################################################################################

#print(soup.prettify())

##################################################################################
### scrape hotel informations
"""
###################
hotel : (cards) -> xpath = //c-wiz[@class="f1dFQe"]
next : (buton) -> xpath = //span[@class="RveJvd snByac"][text() = 'Next']
###################
imgs{}:(urls) -> xpath = //img[@class="x7VXS U106ic q5P4L"]
name:(string) -> xpath = //h2[@class="BgYkof ogfYpf ykx2he"]
rating:(string) -> xpath = //span[@class="KFi5wf lA0BZ"]
Amenities : (list) -> xpath = //span[@class="LtjZ2d sSHqwe ogfYpf"]
price{2}:(string) -> //div/div/div/span/span/span[@jsaction="mouseenter:JttVIc;mouseleave:VqIRre;"]
###################
"""
URL="https://www.google.com/travel/hotels/Morocco?q=hotel%20reservation%20in%20morocco&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4401769%2C4429192%2C4597339%2C4640247%2C4647135%2C4649665%2C4680677%2C4718358%2C4721475%2C4722435%2C4722900%2C4723331%2C4726607%2C4733969%2C4734957%2C4736008%2C4738606&hl=en-MA&gl=ma&ssta=1&rp=ELTG-LSHn7oSELjwmszwnqnCpAEQ3urwv9eR-LJHEJyZ3P3M47yCUjgBQABIAqIBB01vcm9jY28&ap=aAE&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiwrZvFtej2AhUAAAAAHQAAAAAQAg&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESCgoCCAMKAggDEAAaKwoNEgk6B01vcm9jY28aABIaEhQKBwjmDxADGBwSBwjmDxADGB0YATICEAAqCwoHKAE6A01BRBoA"

file=open("hoteles.txt","w")

nbr_hotels=0

def scraping(URL):
    ##################################################################################
    ### downloading a website using the requests.get method
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})
    
    webpage = requests.get(URL, headers=HEADERS)
    ##################################################################################

    ##################################################################################
    ### BeautifulSoup
    soup = BeautifulSoup(webpage.content, "html.parser")

    dom = etree.HTML(str(soup))

    hotels=dom.xpath('//c-wiz[@class="f1dFQe"]')
    global nbr_hotels
    nbr_hotels=nbr_hotels+len(hotels)
    print("\n\n###################")
    print(nbr_hotels)
    print("###################")

    for hotel in hotels:
        names=hotel.xpath('.//h2[@class="BgYkof ogfYpf ykx2he"]')
        ratings=hotel.xpath('.//span[@class="KFi5wf lA0BZ"]')
        prices=hotel.xpath('.//span[@jsaction="mouseenter:JttVIc;mouseleave:VqIRre;"]')
        imgs=hotel.xpath('.//img[@class="x7VXS U106ic q5P4L"]')
    


        for name in names:
            row="\n\nHotel :"+name.text

        for rating in ratings:
            row=row+"\nRating :"+rating.text

        p="None"
        for price in prices:
            if price.text !="None":
                p = price.text
        row=row+"\nPrice :"+str(p)

        row=row+"\nImgs :"
        for img in imgs:
            if img.get("data-src") != "None":
                row=row+"\n "+img.get("data-src")+"\n"


        file.write(row)

while True:
    try:
        def next_page(URL):
            driver = webdriver.Chrome("./chromedriver")
            driver.get(URL)
            sleep(10)
            driver.find_element_by_xpath('//span[@class="RveJvd snByac"][text() ="Next"]').click()
            sleep(10)
            URL=driver.current_url
            print("\n\n",URL)
        
        scraping(URL)
        next_page(URL)
    except:
        print("Erreur!")

file.close()