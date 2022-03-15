

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
# links = ['https://property-nicaragua.com/listing/beachfront-masterpiece/', 'https://property-nicaragua.com/listing/casa-sodi-rancho-santana/', 'https://property-nicaragua.com/listing/oceanfront-surf-masterpiece/']
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

            print("scraping", link)
            print(counter, "of",len(links))
            counter+=1
            try:
                driver.get(link)
                time.sleep(1)



                lcl_title = driver.find_element(By.CSS_SELECTOR,'h1.entry-title')
                lcl_description = driver.find_element(By.CSS_SELECTOR,'div.property-content')


                # address = driver.find_elements(By.CSS_SELECTOR,'div#accordion_prop_addr .listing_detail')
                details = driver.find_elements(By.CSS_SELECTOR,'.property-meta .meta-item')

                lcl_price = driver.find_element(By.CSS_SELECTOR,'span.price')
                lcl_id=driver.find_element(By.CSS_SELECTOR,'span#id-listing')

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

                    if "meta-item-icon icon-area".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_area = value.get_attribute("innerHTML").replace('<sub class="meta-item-unit">', '').replace('</sub>','')
                    if "meta-item-icon icon-bed".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_bedrooms = value.get_attribute("innerHTML")
                    if "meta-item-icon icon-bath".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_bathrooms = value.get_attribute("innerHTML")
                    if "meta-item-icon icon-ptype".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_type = value.get_attribute("innerHTML")
                    if "meta-item-icon icon-tag".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_status = value.get_attribute("innerHTML")
                    if "Total".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_property_size = value.get_attribute("innerHTML").replace('<sub class="meta-item-unit">', '').replace('</sub>','')
                    if "Interior".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_interior = value.get_attribute("innerHTML").replace('<sub class="meta-item-unit">', '').replace('</sub>','')
                    if "Exterior".lower() in el.lower():
                        value = detail.find_element(By.CSS_SELECTOR,"span.meta-item-value")
                        lcl_exterior = value.get_attribute("innerHTML").replace('<sub class="meta-item-unit">', '').replace('</sub>','')

                # return

                item = {
                    "title":lcl_title.text,
                    "description":lcl_description.text,
                    "price":lcl_price.text,

                    "id":lcl_id.text,
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
                    "status":lcl_status,
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






url = "https://property-nicaragua.com/?s=&property_id=&min_sqft=&property_status=0&min_price=0&property_type=houses&min_beds=0&exclusives=3&max_price=0&property_location=0&min_baths=0&s-old=property_search&sort_by=price&sort_dir=DESC&limit=&beaches=0&surfs=0&developments=0&areas=0"
driver.get(url)

def get_all_links():

    try:

        loader = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listings"))
        )

        main = driver.find_elements(By.CSS_SELECTOR, '.listings .property-listing-simple')

        print(len(main), "length of main")

        if len(main) == 0: driver.quit()

        for x in main:
            site_element = x.find_element(By.TAG_NAME, 'a')
            a = site_element.get_attribute('href')
            # print(a)
            links.append(a)

        # Test
        #scrapehouses()
        #return
        # Test

        next_button = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div[3]/form/div[1]/div/button[6]")
        is_disabled = next_button.get_attribute("disabled")
        print(is_disabled,"is_disabled")
        if is_disabled:
            print("links", links)
            scrapehouses()
            return
        next_button.click()
        get_all_links()

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
    collection_name = dbname["propertynicargua"]
    get_all_links()

# get_all_links()
# scrapehouses()
