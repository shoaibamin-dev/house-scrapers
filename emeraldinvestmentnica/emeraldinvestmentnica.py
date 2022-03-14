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
# links =[ 'https://emeraldinvestmentnica.com/real-estate/listing-preview/las-lajas-home', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/mango-land-home', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/seaside-land', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/jiquelite-lot', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/popoyo-hill', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/las-lajas-lots', 'https://emeraldinvestmentnica.com/real-estate/listing-preview/playa-rosada']

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
            
            lcl_title = driver.find_element(By.XPATH,'/html/body/div[1]/section[2]/div/div[1]/div/div[1]/a/h3')
            lcl_description = driver.find_element(By.CSS_SELECTOR,'div.descp-text')
            lcl_price = driver.find_element(By.CSS_SELECTOR,'div.rate-info h5')
            lcl_status = driver.find_element(By.CSS_SELECTOR,'span.purpose-for-sale')

            # print(lcl_title.text, "lcl_title")
            # print(lcl_description.text, "lcl_description")
            # print(lcl_price.text, "lcl_price")
            # print(lcl_status.text, "lcl_status")

         

            details = driver.find_elements(By.CSS_SELECTOR,"div.property-hd-sec li")
          
            for detail in details:
                
                if "bathroom" in detail.text.lower():
                    lcl_bathrooms =  detail.text
                
                if "bed".lower() in  detail.text.lower():
                    lcl_bedrooms =  detail.text
                
                if "area".lower() in detail.text.lower():
                    lcl_area =  detail.text
                        

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
        

    


        




url = "https://emeraldinvestmentnica.com/real-estate/properties/"
driver.get(url)

def get_all_links(page_counter=1):

    try: 

        try:
            loader = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-products"))
            )
        except:
            return

        
       
        main = driver.find_elements(By.CSS_SELECTOR, '.list-products .card')
        
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
        
        try:
            next = driver.find_element(By.CSS_SELECTOR,'a[rel="next"]')
            href = next.get_attribute('href')
            driver.get(href)
            get_all_links(next)
        except:
            scrapehouses()


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
        pass
        # driver.quit()
        # scrapehouses()
        # print(links)
       
get_all_links()
# scrapehouses()