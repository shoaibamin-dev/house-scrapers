from ast import Try
from dataclasses import replace
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import sys
from datetime import datetime
import unicodedata 
import json



driver = webdriver.Chrome("C:\\Program Files\\chromedriver.exe")
driver.maximize_window()


page_counter=1

# Columns
# id = ""
# title =""
# description =""
# price =""
# bedrooms =""
# bathrooms =""
# property_size=""
# property_lot_size=""
# address =""
# city=""
# area=""
# state=""
# country=""
# sold = ""

items = []
links = ['https://nicaliferealty.com/property/two-homes-on-two-acres-seller-financing-available/']
# links =[ 'https://nicaliferealty.com/property/just-reduced-from-279k-sky-house-at-brisas-del-pacifico/','https://nicaliferealty.com/property/50-acre-farm-with-two-houses-and-800-fruit-trees/','https://nicaliferealty.com/property/just-reduced-from-750k-verdemar-villa-14-relaxed-luxury-lifestyle-in-guacalito-de-la-isla/']


dbname = None
collection_name = None

# links.append("https://trinityrealestatenicaragua.com/estate_property/beach-front-5-bedrooms-house-casa-serena-in-san-juan-del-sur-rivas-nicaragua/")


house_types = [
        {
        "url": "https://nicaliferealty.com/property-type/house/",
        "type": "house"
        },
         {
        "url": "https://nicaliferealty.com/property-type/condo-town-home/",
        "type": "condo"
        },
        {
        "url": "https://nicaliferealty.com/property-type/lot-raw-land/",
        "type": "lot-land"
        },
        {
        "url": "https://nicaliferealty.com/property-type/commercial/",
        "type": "commercial"
        }
    ]


def get_database():
    from pymongo import MongoClient
    CONNECTION_STRING = 'mongodb+srv://minhal:minhal123@cluster0.jkar1.mongodb.net/houses-scraper?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)

    return client['houses_sites']

def scrapehouses(type):
    counter = 1

    try:

        for link in links:
            
            print("scraping", link)
            print(counter, "of",len(links))
            counter+=1

            driver.get(link)
            time.sleep(3)

            lcl_id=""
            lcl_address=""
            lcl_state=""
            lcl_city=""
            lcl_country=""
            lcl_property_size=""
            lcl_property_lot_size=""
            lcl_bedrooms=""
            lcl_bathrooms=""
            lcl_area = ""
            lcl_type = ""
            lcl_status = ""
            lcl_interior = ""
            lcl_exterior = ""
            
            lcl_title = driver.find_element(By.CSS_SELECTOR,'h1.page-title')
            print(lcl_title,"lcl_title")
            lcl_description = driver.find_element(By.CSS_SELECTOR,'div.content')
            print(lcl_description,"lcl_description")
            lcl_price = driver.find_element(By.CSS_SELECTOR,'span.price-and-type')
            print(lcl_price,"lcl_price")
            lcl_status = driver.find_element(By.CSS_SELECTOR,'span.status-label ')
            print(lcl_status,"lcl_status")


            details = driver.find_element(By.CSS_SELECTOR,"div.property-meta")
            details_spans = details.find_elements(By.TAG_NAME,"span")

            print(details.text,"details")
            
            for detail in details_spans:
                
                el = detail.get_attribute("outerHTML")

                if "property-meta-size".lower() in el.lower():
                    lcl_area = unicodedata.normalize("NFKD", detail.get_attribute("innerText"))
                if "property-meta-bedrooms".lower() in el.lower():
                    lcl_bedrooms = unicodedata.normalize("NFKD", detail.get_attribute("innerText"))
                if "property-meta-bath".lower() in el.lower():
                    lcl_bathrooms = unicodedata.normalize("NFKD", detail.get_attribute("innerText"))
                if "property-meta-lot-size".lower() in el.lower():
                    lcl_property_lot_size = unicodedata.normalize("NFKD", detail.get_attribute("innerText"))


                        

            item = {
                "title":lcl_title.text,
                "description":lcl_description.text,
                "price":lcl_price.text,
                "id":lcl_id, 
                "bedrooms":lcl_bedrooms,
                "bathrooms":lcl_bathrooms,
                "property_size":lcl_property_size,
                "interior":lcl_interior,
                "exterior":lcl_exterior,
                "property_lot_size":lcl_property_lot_size,
                "address":lcl_address,
                "city":lcl_city,
                "state":lcl_state,
                "country":lcl_country,
                "area":lcl_area,
                "type":lcl_type,
                "status":lcl_status.text,
                "created_at":str(datetime.now()),
                "type":type
            }

            items.append(item)
            print(item, "item")
        # with open('data.json', 'w') as outfile:
        #     json_items = json.dumps(items, indent = 4)
        #     outfile.write(json_items)


    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        
        print("Exception object: ", type(e).__name__)
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        driver.quit()

    finally:
        driver.quit()
        
def get_all_types(type_counter = 0):


    if type_counter >= len(house_types): scrapehouses()

    
    try:   
        get_all_links(house_types[type_counter]["url"], house_types[type_counter]["type"])
        get_all_types(type_counter+1)

    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
       
    finally:
        pass

    

def get_all_links(url,type,page_counter=1):

    
    url1 = f"{url}/page/{page_counter}"
    driver.get(url1)

    try: 

        try:
            loader = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-container"))
            )
        except:
            return

        main = driver.find_elements(By.CSS_SELECTOR, '.list-container .property-item-wrapper')
        
        print(len(main), "length of main")

        if len(main) == 0:
            scrapehouses(type)
            return

        for x in main:
            site_element = x.find_element(By.TAG_NAME, 'a')     
            a = site_element.get_attribute('href')
            links.append(a)

        # Test
        scrapehouses("house")
        # return
        # Test

        # get_all_links(url,type,page_counter+1)

    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)

        # scrapehouses(type)
  
    finally:
        # driver.quit()
        scrapehouses(type)
        # print(links)

if __name__ == "__main__": 
    print('name')   
    dbname = get_database()
    collection_name = dbname["nicaliferealty"]
    print('get_all_links')
    get_all_types()   
    # scrapehouses('house')

# scrapehouses()