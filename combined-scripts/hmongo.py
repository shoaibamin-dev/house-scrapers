from hemail import send


def import_mongo(collection_name, items):

    for item in items:
    
        key = {'url':item["url"]}
        new = collection_name.find_one(key)
        if new is None:
            collection_name.insert_one(item)
            continue

       
        dict1 = new
        dict2 = item
        set1 = set(dict1.items())
        set2 = set(dict2.items())
        diff = (set2 - set1)
        if len(diff) > 1:
            
            message = "HOUSE SCRAPERS - You have the following changes:\n"
            message += "URL - "+new["url"]
            message_html = "<h2>URL - "+new["url"]+"</h2>"
            
            
            for d in diff:
                l = list(d)
                message_html += "\n     <p>The attribute <b>"+l[0]+"</b> is changed from <b>"+l[1]+"</b> to <b>"+new[l[0]]+"</b>.</p>"
                message += "\n     The attribute "+l[0]+" is changed from "+l[1]+" to "+new[l[0]]+"."
        
        
            message_template = """\
                                <!DOCTYPE html>
                                <html>
                                    <body>
                                        <h1 style="color:SlateGray;">You have an updates from House Scraper</h1>
                                        """+message_html+"""
                                    </body>
                                </html>
                                """
            send(message, message_template)

        print(len(diff), diff)
        
      
    print("MongoDB import completed")

