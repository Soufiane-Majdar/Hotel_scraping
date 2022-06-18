
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from lxml import etree
import requests
import json
  

URL="https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaIwBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuALAy8iUBsACAdICJDI0NWUxZTk0LWY2MjMtNGM1ZC1iMWVlLWY0YzMyY2EwYzFhNtgCBOACAQ&lang=en-gb&sid=594b058a03c7bbbf9e5ea9dde3037916&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D304142%26label%3Dgen173nr-1DCAEoggI46AdIM1gEaIwBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuALAy8iUBsACAdICJDI0NWUxZTk0LWY2MjMtNGM1ZC1iMWVlLWY0YzMyY2EwYzFhNtgCBOACAQ%26sid%3D594b058a03c7bbbf9e5ea9dde3037916%26sb_price_type%3Dtotal%3Bsrpvid%3Dadca61d3c34b03ce%26%26&ss=Morocco&is_ski_area=&ssne=Essaouira&ssne_untouched=Essaouira&checkin_year=2022&checkin_month=6&checkin_monthday=11&checkout_year=2022&checkout_month=6&checkout_monthday=12&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=mor&ac_position=0&ac_langcode=en&ac_click_type=b&dest_id=143&dest_type=country&place_id_lat=32.4281&place_id_lon=-6.92197&search_pageview_id=a18863b1e51d0383&search_selected=true&search_pageview_id=a18863b1e51d0383&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"

file=open("hoteles.txt","w")

nbr_hotels=0

N_H=0


# first page 
H ="//div[@class='d20f4628d0']"
H_link =".//a[@data-testid='title-link']/@href"
H_name =".//div[@data-testid='title']"
H_price =".//span[@class='fcab3ed991 bd73d13072']"
H_rate =".//div[@class='b5cd09854e d10a6220b4']"
H_reviews =".//div[@class='d8eab2cf7f c90c0a70d3 db63693c62']"
H_image =".//img[@class='b8b0793b0e']/@src"

# in about page hotel
H_adress ="//span[@data-node_tt_id='location_score_tooltip']"
H_map_box ="//span[@data-node_tt_id='location_score_tooltip']/@data-bbox"


H_Description ="//div[@class='bui-grid__column bui-grid__column-8 k2-hp--description']"
H__facilities ="(//div[@data-et-view='goal:hp_d_property_popular_facilities_seen'])[1]/div"



HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})

Hotel = {
    'name':'',
    'price':'',
    'rating':'',
    'review':'',
    'img':'',
    'adress':'',
    'map_X':'',
    'map_Y':'',
    'Description':'',
    'facilities':''
    }

# function to add to JSON
def write_json(new_data, filename='Hotel.json'):
     with open(filename,'r+') as file:
           # First we load existing data into a dict.
         file_data = json.load(file)
         # Join new_data with file_data inside emp_details
         file_data["Hotels"].append(new_data)
         # Sets file's current position at offset.
         file.seek(0)
         # convert back to json.
         json.dump(file_data, file, indent = 4)



def about(link):
    ##################################################################################
    ### downloading a website using the requests.get method

    webpage = requests.get(link, headers=HEADERS)
    ##################################################################################

    ##################################################################################
    ### BeautifulSoup
    soup = BeautifulSoup(webpage.content, "html.parser")

    dom = etree.HTML(str(soup)) 

    adress=dom.xpath(H_adress)
    map_box=dom.xpath(H_map_box)
    Description=soup.find('div',id='property_description_content')
    facilities=soup.find('div',{"data-et-view": "goal:hp_d_property_popular_facilities_seen"})


    for a in adress:
        print("\n\n adress : \n"+a.text)
        Hotel["adress"]=a.text

    for map in map_box:
        print("\n\n adress map : ")
        print("     X : "+map.split(",")[0])
        print("     Y : "+map.split(",")[1])
        Hotel["map_X"]=map.split(",")[0]
        Hotel["map_Y"]=map.split(",")[1]
    
    des=""
    
    for d in Description: 
        if d != "":
            des=des+str(d).strip('\n')
    
    D=des.split("</p>", 1)
    print("\n\n Description : \n"+D[1])
    Hotel["Description"]=str(D[1])

    fs=""
    for f in facilities: 
        if f != "":
            fs=fs+str(f).strip('\n')
    F=fs.split("</h3>", 1)
    print("\n\n facilities : \n"+F[1])
    Hotel["facilities"]=str(F[1])

    write_json(Hotel)

            

def scraping(URL):
    ##################################################################################
    ### downloading a website using the requests.get method

    webpage = requests.get(URL, headers=HEADERS)
    ##################################################################################

    ##################################################################################
    ### BeautifulSoup
    soup = BeautifulSoup(webpage.content, "html.parser")

    dom = etree.HTML(str(soup))

    hotels=dom.xpath(H)
    global nbr_hotels
    nbr_hotels=nbr_hotels+len(hotels)

    print("\n\n###################")
    print(nbr_hotels)
    print("###################")

    for hotel in hotels:
        links=hotel.xpath(H_link)
        names=hotel.xpath(H_name)
        prices=hotel.xpath(H_price)
        ratings=hotel.xpath(H_rate)
        reviews=hotel.xpath(H_reviews)
        imgs=hotel.xpath(H_image)
    
        print("\n\n\n######################################################################################################")
        global N_H
        N_H = N_H+1
        print("Hotel :"+str(N_H))
        print("########################################")


        for n in names:
                print("\n\n name : \n"+n.text)
                Hotel["name"]=n.text
        
        for p in prices:
                print("\n\n price : \n"+p.text)
                Hotel["price"]=p.text.replace("\u00A0"," ")

        for rt in ratings:
                print("\n\n rating : \n"+rt.text)
                Hotel["rating"]=rt.text

        for rv in reviews:
                print("\n\n review : \n"+rv.text)
                Hotel["review"]=rv.text
        
        for img in imgs:
                print("\n\n img : \n"+img)
                Hotel["img"]=img

        for l in links:
            about(l)
            
def next_page(URL):
        driver = webdriver.Chrome("./chromedriver101")
        driver.get(URL)
        sleep(20)
        driver.find_element_by_xpath('//button[@aria-label="Next page"]').click()
        sleep(20)
        URL=driver.current_url
        print("\n\n ###########  New Page ###########")

while True:
    try:
        scraping(URL)
        next_page(URL)

    except Exception as e:
        print("Erreur :",e)


