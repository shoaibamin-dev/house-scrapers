
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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
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



dbname = None
collection_name = None


def get_database():
    from pymongo import MongoClient

    CONNECTION_STRING = 'mongodb+srv://minhal:minhal123@cluster0.jkar1.mongodb.net/property-scrapers-aws?retryWrites=true&w=majority'


    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client['property-scrapers-aws']

def import_mongo():


    for item in items:
        key = {'url':item["url"]}
        collection_name.replace_one(key,item,upsert=True);

    print("MongoDB import completed")



def scrapehouses():
    counter = 1

    try:
        for link in links:

            try:

                print("scraping", link)
                print(counter, "of",len(links))
                counter+=1

                driver.get(link)
                time.sleep(1)
                loader = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,'entry-title'))
                )
                lcl_title = driver.find_element(By.CSS_SELECTOR,'h1.entry-title')
                lcl_price = driver.find_element(By.CSS_SELECTOR,'span.price_area')
                lcl_description = driver.find_element(By.CSS_SELECTOR,'div.wpestate_property_description')
                lcl_sold = driver.find_element(By.CSS_SELECTOR,'div.slider-property-status')


                address = driver.find_elements(By.CSS_SELECTOR,'div#accordion_prop_addr .listing_detail')
                details = driver.find_elements(By.CSS_SELECTOR,'div#accordion_prop_details .listing_detail')

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

                for addr in address:
                    if "Address".lower() in addr.text.lower():
                        lcl_address = addr.text
                    if "City".lower() in addr.text.lower():
                        lcl_city = addr.text
                    if "State/County".lower() in addr.text.lower():
                        lcl_state = addr.text
                    if "Country".lower() in addr.text.lower():
                        lcl_country = addr.text
                    if "Area".lower() in addr.text.lower():
                        lcl_area = addr.text

                for detail in details:
                    if "Property Id".lower() in detail.text.lower():
                        lcl_id = detail.text
                    if "Property Lot Size".lower() in detail.text.lower():
                        lcl_property_lot_size = detail.text
                    if "Property Size".lower() in detail.text.lower():
                        lcl_property_size = detail.text
                    if "Bedrooms".lower() in detail.text.lower():
                        lcl_bedrooms = detail.text
                    if "Bathrooms".lower() in detail.text.lower():
                        lcl_bathrooms = detail.text



                item = {
                    "title":lcl_title.text,
                    "description":lcl_description.text,
                    "price":lcl_price.text,

                    "id":lcl_id,
                    "bedrooms":lcl_bedrooms.replace('Bedrooms: ',''),
                    "bathrooms":lcl_bathrooms.replace('Bathrooms: ',''),
                    "property_size":lcl_property_size.replace('Property Size: ',''),
                    "property_lot_size":lcl_property_lot_size.replace('Property Lot Size: ',''),
                    "address":lcl_address.replace('Address: ',''),
                    "city":lcl_city.replace('City: ',''),
                    "state":lcl_state.replace('State/County: ',''),
                    "country":lcl_country.replace('Country: ',''),
                    "area":lcl_area.replace('Area: ',''),

                    "sold":"Y" if "Sold" in lcl_sold.text.lower() else "N",
                    "created_at":str(datetime.now()),
                        "url":link
                }

                items.append(item)

            except Exception as e:
                 continue

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


    finally:
        driver.quit()
        print("finally")
        if items:
            import_mongo()







def get_all_links(page_counter=1):

    url = "https://trinityrealestatenicaragua.com/property_category/houses/page/"+str(page_counter)
    driver.get(url)



    try:

        loader = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listing_wrapper"))
        )

        main = driver.find_elements(By.CLASS_NAME, 'listing_wrapper')

        print(len(main), "length of main")

        if len(main) == 0: driver.quit()

        # ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()

        for x in main:

            site_element = x.find_element(By.TAG_NAME, 'a')

            a = site_element.get_attribute('href')
            links.append(a)

        # Test
        #scrapehouses()
        #return
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

if __name__ == "__main__":
    dbname = get_database()
    collection_name = dbname["trinityrealestatenicaragua"]
    get_all_links()

# get_all_links(1)

