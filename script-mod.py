from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep
'''
from fake_useragent import UserAgent
import os
import sqlite3
import shutil
from stem import Signal
from stem.control import Controller
import socket
import socks

controller = Controller.from_port(port=9051)
controller.authenticate()'''

req = requests.Session()
base_url = 'https://www.ericjackson.com'
'''
def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
hdr = {'User-Agent': UA.random}'''
hdr = {'User-Agent': 'Mozilla/5.0'}

def get_html(url):
    
    html_content = ''
    try:
        page = req.get(url, headers=hdr)
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_value(html, info_name):
    
    info_value = None
       
    try:
        info_items = html.select('.LabelText')
        for info_item in info_items:
            info_text = info_item.get_text().strip()
            if info_name in info_text:
                info_value = info_text.replace(info_name, '').strip()
                break
    except:
        pass
    
    return info_value 

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        title = html.select('.DetailTitle')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None      
    
    try:
        raw_text = html.select('.ProductDetails')[0].get_text().strip()
        stamp['raw_text'] = raw_text.replace('"',"'")
    except:
        stamp['raw_text'] = None
    
    try:
        price = html.select('p .PriceUser')[0].get_text().strip()
        price = price.replace('Price $ ', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
        
    stamp['condition'] = get_value(html, 'Condition') 
    stamp['grade'] = get_value(html, 'Grade')
    
    try:
        category = html.select('.BreadCrumb a')[1].get_text().strip()
        stamp['category'] = category
    except:
        stamp['category'] = None
        
    stamp['base_category'] = selection  
       
    try:
        subcategory = html.select('.BreadCrumb a')[2].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None     
        
       

    stamp['currency'] = 'USD'
    
    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('form tr td img')
        for image_item in image_items:
            img_src = image_item.get('src')
            if 'Ext.JPG' in img_src:
                img = base_url + '/' + img_src
                if img not in images:
                    images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('td a.head2'):
            item_link = base_url + '/' + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_items = html.select('a.NavBar')
        for next_item in next_items:
            next_text = next_item.get_text().strip()
            next_href = next_item.get('href')
            if((next_text == 'Next >>') and (next_href != 'javascript:void(0)')):
                next_url = base_url + next_href
    except:
        pass   
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories(url, element_class):
   
    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('a.' + element_class):
            item_link = base_url  + '/' + item.get('href')
            if item_link not in items: 
                items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items
'''
def file_names(stamp):
    file_name = []
    rand_string = "RAND_"+str(randint(0,100000000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    print (file_name)
    return(file_name)

def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM eric_jackson WHERE {cn} == "{un}" AND {cn2} == "{un2}"'.format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2))
    all_rows = c.fetchall()
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        try:
            conn1.commit()
            conn1.close()
        except:
            conn1.commit()
            conn1.close()
        print (" ")
        sleep(randint(35,100))
        next_step = 'continue'
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        try:
            conn2.commit()
            conn2.close()
        except:
            conn2.commit()
            conn2.close()
        next_step = 'pass'
    print("Price Updated")
    return(next_step)

def db_update_image_download(stamp): 
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/eric_jackson/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    names = file_names(stamp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    image_paths = [directory + names[i] for i in range(len(names))]
    for item in range(0,len(names)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=120, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=120, stream=True)
        if imgRequest1.status_code==200:
            with open(names[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    database_update =[]
    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['base_category'],
        stamp['category'],
        stamp['subcategory'],
        stamp['condition'],
        stamp['grade'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO eric_jackson ('url','raw_text', 'title','base_category','category','subcategory',
    'condition','grade','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    try:
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
    print ("all updated")
    print ("++++++++++++")
    print (" ")
    sleep(randint(55,160)) 

connectTor()
count = 0'''

item_dict = {
"United States": "https://www.ericjackson.com/rHome1d.asp?Header=USA&x=",
"U.S. Possessions": "https://www.ericjackson.com/rhome1c.asp?Header=US_POSS&x=",
"U.S. State Revenues": "https://www.ericjackson.com/rHome1d.asp?Header=State_Rev&x=",
"U.S. State Fish & Game Stamps": "https://www.ericjackson.com/rHome1d.asp?Header=State_F_G&x=",
"League of Nations": "https://www.ericjackson.com/rHome1d.asp?Header=League_Nations&x=",
"Allied Military Government": "https://www.ericjackson.com/rHome1d.asp?Header=AMG&x=",
"Canada": "https://www.ericjackson.com/rHome1d.asp?Header=Canada&x=",
"Canada Provinces": "https://www.ericjackson.com/rHome1d.asp?Header=Can_Provi&x=",
"Great Britain": "https://www.ericjackson.com/rHome1d.asp?Header=GB&x=",
"British": "https://www.ericjackson.com/rHome1d.asp?Header=Can_Provi&x=",
"British Africa": "https://www.ericjackson.com/rHome1d.asp?Header=BC-Africa&x=",
"British America": "https://www.ericjackson.com/rHome1d.asp?Header=BritishAmerica&x=",
"British Asia": "https://www.ericjackson.com/rHome1d.asp?Header=BC_Asia&x=",
"British Europe": "https://www.ericjackson.com/rHome1d.asp?Header=BC_Europe&x=",
"British Middle East": "https://www.ericjackson.com/rHome1d.asp?Header=BR_MIDDLE_EAST&x=",
"British Oceania": "https://www.ericjackson.com/rHome1d.asp?Header=BC_Oceania&x=",
"British West Indies": "https://www.ericjackson.com/rHome1d.asp?Header=BC_West_Indies&x=",
"WORLDWIDE": "https://www.ericjackson.com/rHome1d.asp?Header=WORLD&x=",
"Revenue Stamped Paper Specialized": "https://www.ericjackson.com/rHome1d.asp?Header=RSP_Spec&x=",
"Postal History": "https://www.ericjackson.com/rHome1d.asp?Header=PostalHistory&x=",
"Collections and Accumulations": "https://www.ericjackson.com/rHome1d.asp?Header=CollectionsandAccumulatio&x="
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose category: ')

selected_main_category = item_dict[selection]

categories = get_categories(selected_main_category, 'HeadCat')   
for category in categories:
    subcategories = get_categories(category, 'HeadSub') 
    for subcategory in subcategories:
        page_url = subcategory
        while(page_url):
            page_items, page_url = get_page_items(page_url)
            for page_item in page_items:
                '''count += 1
                if count > randint(30,156):
                    print('Sleeping...')
                    sleep(randint(1000, 4000))
                    hdr['User-Agent'] = UA.random
                    renew_tor()
                    connectTor()
                    count = 0
                else:
                    pass'''
                stamp = get_details(page_item)
                '''if stamp['price']==None or stamp['price']=='':
                    sleep(randint(500,700))
                    continue
                next_step = query_for_previous(stamp)
                if next_step == 'continue':
                    print('Only updating price')
                    continue
                elif next_step == 'pass':
                    print('Inserting the item')
                    pass
                else:
                    break
                db_update_image_download(stamp)
                sleep(randint(10,30))'''
print('Scrape Complete!')