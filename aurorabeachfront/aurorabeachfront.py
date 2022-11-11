from ast import Try
from asyncio.windows_events import NULL
from dataclasses import replace
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json;

import time
import sys
from datetime import datetime


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

links = []
# links =["https://aurorabeachfront.com/nicaraguarealestate/property/showproperty.php?id=109"]


items = []

dbname = None
collection_name = None


def get_database():
    from pymongo import MongoClient
    CONNECTION_STRING = 'mongodb+srv://minhal:minhal123@cluster0.jkar1.mongodb.net/houses-scraper?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)

    return client['houses_sites']
    


def scrapehouses(type):
    global dbname
    global collection_name
    counter = 1
    try:
        for link in links:
            
            try:
                print("scraping", link)
                print(counter, "of",len(links))
                counter+=1

                driver.get(link)
                time.sleep(1)


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
                
                lcl_title = driver.find_element(By.CSS_SELECTOR,'h1.widget-title span')
                lcl_description = driver.find_element(By.CSS_SELECTOR,'aside#listify_widget_panel_listing_content-2')
                lcl_price = driver.find_element(By.CSS_SELECTOR,'h1.widget-title')
                lcl_sold = ""

                try:
                    lcl_sold = driver.find_element(By.CSS_SELECTOR, "div.pstatus").text
                except:
                    pass


                details = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/main/aside[1]/div[1]")

                "Listing #2573 | Bedrooms: 4 | Bathrooms: 3.5 | Location: North of San Juan del Sur details"
                details_text = details.text


                dsplit = details_text.split("|")

            


                for d in dsplit:
                    if "Listing" in d:
                        lcl_id = d.replace("Listing",'')
                    if "Bedrooms" in d:
                        lcl_bedrooms = d.replace("Bedrooms:",'')
                    if "Bathrooms" in d:
                        lcl_bathrooms = d.replace("Bathrooms:",'')
                    if "Location" in d:
                        lcl_address = d
                    if "Lot Size" in d:
                        lcl_property_lot_size = d.replace("Lot Size:",'')

                            
                item = {
                    "title":lcl_title.text.strip(),
                    "description":lcl_description.text.strip(),
                    "price":lcl_price.text.strip(),
                    "id":lcl_id.strip(), 
                    "bedrooms":lcl_bedrooms.strip(),
                    "bathrooms":lcl_bathrooms.strip(),
                    "property_size":lcl_property_size.strip(),
                    "interior":lcl_interior.strip(),
                    "exterior":lcl_exterior.strip(),
                    "property_lot_size":lcl_property_lot_size.strip(),
                    "address":lcl_address.strip(),
                    "city":lcl_city.strip(),
                    "state":lcl_state.strip(),
                    "country":lcl_country.strip(),
                    "area":lcl_area.strip(),
                    "type":lcl_type.strip(),
                    "status":lcl_sold.strip(),
                    "created_at":str(datetime.now()),
                    "url":link,
                    "house_kind":type
                }

                print(item, "item")
                collection_name.insert_one(item)
                
            except:
                continue
                
            # items.append(item)

        # with open('data.json', 'w') as outfile:
        #     json_items = json.dumps(items, indent = 4)
        #     outfile.write(json_items)

    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        driver.quit()

    
house_types = [
        {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/houses.php",
        "type": "house"
        },
         {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/lots.php",
        "type": "lots"
        },
        {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/condos.php",
        "type": "condos"
        },
        {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/surf.php",
        "type": "surf"
        },
        {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/beachfront.php",
        "type": "beachfront"
        },
        {
        "url": "https://aurorabeachfront.com/nicaraguarealestate/commercial.php",
        "type": "commercial"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/acreages.php",
        "type": "acreages"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/sanjuandelsur.php",
        "type": "sanjuandelsur"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/exclusives.php",
        "type": "exclusives"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/featured.php",
        "type": "featured"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/green.php",
        "type": "green"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/golf.php",
        "type": "golf"
        },
         {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/developments.php",
        "type": "developments"
        },
        {
        "url":  "https://aurorabeachfront.com/nicaraguarealestate/newest.php",
        "type": "newest"
        }
    ]

current_type = "house"
     
def get_all_types(type_counter = 0):

    global current_type

    if type_counter >= len(house_types): return

    current_type = house_types[type_counter]["type"]

    print(current_type, "current_type")

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
    
    print(url, 'url')
    driver.get(url)

    try: 

        loader = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job_listings"))
        )
       
        main = driver.find_elements(By.CSS_SELECTOR, '.job_listings li')
        
        print(len(main), "length of main")

        if len(main) == 0:
            scrapehouses()
            return

        for x in main:
            site_element = x.find_element(By.TAG_NAME, 'a')     
            a = site_element.get_attribute('href')
            links.append(a)

        # Test
        # scrapehouses()
        # return
        # Test

        get_all_links(page_counter + 1)

    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        
        print(links, "links")

        scrapehouses(type)
        # driver.quit()
       
    finally:
        pass
       

if __name__ == "__main__": 
    print('name')   
    dbname = get_database()
    collection_name = dbname["aurorabeachfront"]
    print('get_all_links')
    get_all_types()   
    # get_all_links()
# scrapehouses()