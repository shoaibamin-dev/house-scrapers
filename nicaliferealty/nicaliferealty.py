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
links = []
# links =[ 'https://nicaliferealty.com/property/just-reduced-from-279k-sky-house-at-brisas-del-pacifico/','https://nicaliferealty.com/property/50-acre-farm-with-two-houses-and-800-fruit-trees/','https://nicaliferealty.com/property/just-reduced-from-750k-verdemar-villa-14-relaxed-luxury-lifestyle-in-guacalito-de-la-isla/']

def scrapehouses():
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
            lcl_description = driver.find_element(By.CSS_SELECTOR,'div.content')
            lcl_price = driver.find_element(By.CSS_SELECTOR,'span.price-and-type')
            lcl_status = driver.find_element(By.CSS_SELECTOR,'span.status-label ')


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
                "created_at":str(datetime.now())
            }

            items.append(item)

        with open('data.json', 'w') as outfile:
            json_items = json.dumps(items, indent = 4)
            outfile.write(json_items)


    except Exception as e:
        print("Error:",e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        driver.quit()

    finally:
        driver.quit()
        

    


        





def get_all_links(page_counter=1):

    
    url = f"https://nicaliferealty.com/property-type/house/page/{page_counter}"
    driver.get(url)

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
            scrapehouses()
            return

        for x in main:
            site_element = x.find_element(By.TAG_NAME, 'a')     
            a = site_element.get_attribute('href')
            links.append(a)

        # Test
        scrapehouses()
        return
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

        scrapehouses()

        
        
       
    finally:
        # driver.quit()
        scrapehouses()
        # print(links)
       
get_all_links()
# scrapehouses()