from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import sys
from datetime import datetime 
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
# links.append("https://trinityrealestatenicaragua.com/estate_property/beach-front-5-bedrooms-house-casa-serena-in-san-juan-del-sur-rivas-nicaragua/")

def scrapehouses():
    counter = 1

    try:
        for link in links:

            print("scraping", link)
            print(counter, "of",len(links))
            counter+=1


            driver.get(link)
            time.sleep(3)
            
            lcl_title = driver.find_element(By.CSS_SELECTOR,'h1.text-primary')
            lcl_description = driver.find_element(By.CSS_SELECTOR,'section#propertyDescription')
            # lcl_sold = driver.find_element(By.CSS_SELECTOR,'div.slider-property-status')

            # address = driver.find_elements(By.CSS_SELECTOR,'div#accordion_prop_addr .listing_detail')
            details = driver.find_elements(By.CSS_SELECTOR,'section#propertyDetails .property-stats div')

            lcl_price=""
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

            # print(lcl_bathrooms.text,"lcl_bathrooms")

            # for addr in address:
            #     if "Address".lower() in addr.text.lower():
            #         lcl_address = addr.text
            #     if "City".lower() in addr.text.lower():
            #         lcl_city = addr.text
            #     if "State/County".lower() in addr.text.lower():
            #         lcl_state = addr.text
            #     if "Country".lower() in addr.text.lower():
            #         lcl_country = addr.text
            #     if "Area".lower() in addr.text.lower():
            #         lcl_area = addr.text    

            for detail in details:
                
                el = detail.get_attribute("innerHTML")
                # print(el,"el")

                if "Property ID".lower() in el.lower():
                    lcl_id = detail.text.replace("Property ID",'')
                if "fas fa-expand".lower() in el.lower():
                    lcl_property_size = detail.text
                if "fas fa-bed".lower() in el.lower():
                    lcl_bedrooms = detail.text
                if "fas fa-bath".lower() in el.lower():
                    lcl_bathrooms = detail.text
                if "fas fa-home".lower() in el.lower():
                    lcl_area = detail.text
                if "USD $".lower() in el.lower():
                    lcl_price = detail.text.replace("USD $",'')
              
       
            item = {
                "title":lcl_title.text,
                "description":lcl_description.text,
                "price":lcl_price,

                "id":lcl_id, 
                "bedrooms":lcl_bedrooms,
                "bathrooms":lcl_bathrooms,
                "property_size":lcl_property_size,
                "property_lot_size":lcl_property_lot_size,
                "address":lcl_address,
                "city":lcl_city,
                "state":lcl_state,
                "country":lcl_country,
                "area":lcl_area,
                
                "sold":"N",
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

    


        




def get_all_links(page_counter):

    url = f"https://www.investnicaragua.com/properties/page/{page_counter}"
    driver.get(url)
   


    try: 

        loader = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "archive-property-item"))
        )
       
        main = driver.find_elements(By.CLASS_NAME, 'archive-property-item')
        
        print(len(main), "length of main")

        if len(main) == 0: driver.quit()

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
        pass
        # print(links)
        # scrapehouses()
        # driver.quit()
        
get_all_links(1)
