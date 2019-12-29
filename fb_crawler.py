from bs4 import BeautifulSoup
import requests, time
from selenium import webdriver
 
USERNAME=input("USERNAME:")
PASSWORD=input("PASSWORD:")
link=input("paste you or your friends's fb link here:")
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values':{'notifications': 2}}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path="",options=options)
 
driver.get("https://www.facebook.com")
account = driver.find_element_by_name("email")
account.send_keys(USERNAME)
password = driver.find_element_by_name("pass")
password.send_keys(PASSWORD)
try: # old version
    button = driver.find_element_by_id("loginbutton")
    button.click()
except: # new version
    button = driver.find_element_by_name("login")
    button.click()
   
   
   
   
 
driver.get(link)
for i in range(5):
    driver.execute_script(f"window.scrollTo(0, {5000 * (i + 1)})")
    time.sleep(3)
html = driver.page_source
 
all_post=list()
soup = BeautifulSoup(html, 'html.parser')
divs = soup.find_all('div', class_="text_exposed_root")
 
for div in divs:
    p = div.find_all('p')
    itemm=""
    for item in p:
        item=item.get_text()
        itemm+=item
    all_post.append(itemm)