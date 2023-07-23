import tkinter as tk
from selenium import webdriver
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
import sys




win = tk.Tk()
# Set the geometry of the win
canvas = tk.Canvas(win,width=750,height=600)
canvas.grid(column=7,row=7)
# Create a frame widget
# Create a label widget
titlelabel=tk.Label(win, text="Automated Instagram Bot", font='Arial 17 bold')
titlelabel.place(relx=0.5, rely=0.05, anchor="center")

usernamelabel = tk.Label(win, text='Enter instagram account usernames on each line').place(relx=0.03, rely=0.10)
passwordlabel = tk.Label(win, text='Enter instagram account passwords on each line').place(relx=0.03, rely=0.25)
usernameslabel = tk.Label(win, text='Enter list of usernames on each line').place(relx=0.03, rely=0.4)
hashtagslabel = tk.Label(win, text='Enter list of hashtags on each line').place(relx=0.03, rely=0.55)
locationslabel = tk.Label(win, text='Enter list of location Id on each line').place(relx=0.03, rely=0.70)
e1 = tk.Text(win,width=100)
e2 = tk.Text(win,width=100)
e3 = tk.Text(win,width=100)
e4 = tk.Text(win,width=100)
e5 = tk.Text(win,width=100)
e1.place(relx=0.03, rely=0.13, width=700,height=60)
e2.place(relx=0.03, rely=0.28, width=700,height=60)
e3.place(relx=0.03, rely=0.43, width=700,height=60)
e4.place(relx=0.03, rely=0.58, width=700,height=60)
e5.place(relx=0.03, rely=0.73, width=700,height=60)

def startBot():
    
    accountsusernames = e1.get("1.0", tk.END).splitlines()
    accountpasswords = e2.get("1.0", tk.END).splitlines()
    listofusernames = e3.get("1.0", tk.END).splitlines()
    listofhashtags = e4.get("1.0", tk.END).splitlines()
    listoflocations = e5.get("1.0", tk.END).splitlines()
    
    # Create threads for each account
    threads = []
    for i in range(len(accountsusernames)):
        t = threading.Thread(target=loginAndStartAction, args=(accountsusernames[i], accountpasswords[i], listofusernames, listofhashtags, listoflocations))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        
def loginAndStartAction(username,password,listofusernames,listofhashtags,listoflocations):
    # Perform login using Selenium
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(10)
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']"))).click()
        print('cookie btn',WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']"))))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'_a9--') and contains(@class,'_a9_0')]"))).send_keys(Keys.SPACE)
    #driver.execute_script("arguments[0].scrollIntoView()",cookiebtn)
    #driver.execute_script("arguments[0].click()",cookiebtn)
    # # Find the login elements and enter the username and password
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_input.send_keys(password)

    # # Submit the form to log in
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()
    
    try: 
        Notnow_2fadiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Not Now')]")))
        Notnow_2fadiv.click()
        Notnow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Not Now')]")))
        Notnow_button.click()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    if not listofusernames:
        print(len(listofusernames))
    else:
        for _username in listofusernames:
            performactionsonusernames(_username,driver)
            print(len(listofusernames))
        
    
    if not listofhashtags:
        print(len(listofhashtags))
    else:
        for _hashtag in listofhashtags:
            performactionsonhashtags(_hashtag,driver)
            print(len(listofhashtags))
        
    
    if not listoflocations:
        print(len(listoflocations))
    else:
        for _locationid in listoflocations:
            performactionsonlocations(_locationid,driver)
            print(len(listoflocations))
            

def performactionsonusernames(_username,driver):
    # Enter username account
    driver.get(f'https://www.instagram.com/{_username}/')
    
    time.sleep(10)  # Add a small delay to allow the page to load

    try:
        # click on account profile to show stories
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'_aarf') and contains(@class,'_aarg')]"))).click()
        time.sleep(5)
        
        # get story's count
        # storycounts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class,'_ac3n')]"))).click()
        # like story
        driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
        time.sleep(3)                    
        # close story container
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'xds687c')]//div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]"))).click()
        time.sleep(2)
        
        # max_iterations = 5
        # iterations = 0
        

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    try: 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        followers_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'follower')
        
        followers_link.click()
        time.sleep(10)
        
        max_interations = 15
        iterations = 0
        
        try:
            followers_container = driver.find_element(By.XPATH,"//div[contains(@class,'_aano')]")
            # last_height = driver.execute_script("return arguments[0].scrollHeight", followers_container)

            while iterations < max_interations:
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_container)
                time.sleep(10)

                # new_height = driver.execute_script("return arguments[0].scrollHeight", followers_container)
                iterations += 1
                if iterations == max_interations:
                    break
                
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        followers_usernames_hrefs = []
        followers_list_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@role,'link') and contains(@class, 'x1i10hfl') and contains(@class, 'xjbqb8w') and contains(@class, 'x6umtig') and contains(@class, 'x1b1mbwd') and contains(@class, 'xaqea5y') and contains(@class, 'xav7gou') and contains(@class, 'x9f619') and contains(@class, 'x1ypdohk') and contains(@class, 'xt0psk2') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x16tdsg8') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1a2a7pz') and contains(@class, 'notranslate') and contains(@class, '_a6hd')]")))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        time.sleep(10)
        # print('followers lists',followers_list_links)
        print('followers lists count',len(followers_list_links))
        if len(followers_list_links) > 0:
            for followers_list_link in followers_list_links:
                # get href attribute
                followers_usernames_hrefs.append(followers_list_link.get_attribute('href'))
                # followers_usernames_links.append(username.text)
                # time.sleep(2)

            likefollowersstorys(followers_usernames_hrefs,driver)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def likefollowersstorys(followers_usernames_hrefs,driver):
    
    # print('followers hrefs',followers_usernames_hrefs)
    # print('followers hrefs count',len(followers_usernames_hrefs))
    for followers_usernames_href in followers_usernames_hrefs:
        driver.get(followers_usernames_href)
        # print('followers href',followers_usernames_href)
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'_aarf') and contains(@class,'_aarg')]"))).click()
            time.sleep(5)
            # like story
            driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
            time.sleep(3)
            # close story container
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'xds687c')]//div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]"))).click()
            time.sleep(2)
        except Exception as e:
            # Handle the exception
            print(f"An error occurred: {str(e)}")
        
def performactionsonhashtags(_hashtag,driver):    
    
    try:
        driver.get('https://www.instagram.com/explore/tags/{}/'.format(_hashtag))
        time.sleep(15)
        hashtagposts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/') and contains(@role,'link')]")))
        
        hashtag_posts_links = []
        
        for hashtagpost_link in hashtagposts:
            hashtagpost_href = hashtagpost_link.get_attribute('href')
            hashtag_posts_links.append(hashtagpost_href)
            # like
            time.sleep(5)
            
        likehashtagpostsUserAccountsStory(hashtag_posts_links,driver)    
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def likehashtagpostsUserAccountsStory(hashtag_posts_links,driver):
    # print('hash tag posts links',hashtag_posts_links)
    for hashtag_posts_link in hashtag_posts_links:
        # get account username of the hashtag post
        driver.get(hashtag_posts_link)
        # print('hash tag posts links',hashtag_posts_link)
        time.sleep(5)
        try:
            # like the post first
            driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
            time.sleep(3)
            # get the user account profile
            hashtagpostusername = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'_aaqq') and contains(@role,'button')]")))
            # click on account username profile to open their story 
            hashtagpostusername.click()
            time.sleep(5)
            # like the first story
            driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
            time.sleep(3)
            
            # close story container
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'xds687c')]//div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]"))).click()
            time.sleep(2)
            # driver.find_element(By.XPATH,"//span/button[contains(@class,'_abl-') and contains(@type,'button')]").click()
            # time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {str(e)}")    


def performactionsonlocations(_locationid,driver):    
    
        try:
            driver.get('https://www.instagram.com/explore/locations/{}/'.format(_locationid))
            time.sleep(15)
            
            locationposts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/') and contains(@role,'link')]")))
            
            location_posts_links = []
            
            for locationpost_link in locationposts:
                locationpost_href = locationpost_link.get_attribute('href')
                location_posts_links.append(locationpost_href)
                # like
                time.sleep(5)
                
            likelocationpostsUserAccountsStory(location_posts_links,driver)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def likelocationpostsUserAccountsStory(location_posts_links,driver):
    # print('location id posts links',location_posts_links)
    for location_posts_link in location_posts_links:
        # get account username of the hashtag post
        driver.get(location_posts_link)
        # print('location id posts links',location_posts_link)
        time.sleep(5)
        try:
            # like the post first
            driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
            time.sleep(3)
            # get the user account profile
            hashtagpostusername = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'_aaqq') and contains(@role,'button')]")))
            # click on account username profile to open their story 
            hashtagpostusername.click()
            time.sleep(5)
            # like the first story
            driver.find_element(By.XPATH, "//span/div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]").click()
            time.sleep(3)
            
            # close story container
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'xds687c')]//div[contains(@role,'button') and contains(@class,'x1i10hfl') and contains(@class,'x6umtig')and contains(@class,'x1b1mbwd')and contains(@class,'xaqea5y')and contains(@class,'xav7gou')and contains(@class,'x9f619')and contains(@class,'xe8uvvx')and contains(@class,'xdj266r')and contains(@class,'x11i5rnm')and contains(@class,'xat24cr')and contains(@class,'x1mh8g0r')and contains(@class,'x16tdsg8')and contains(@class,'x1hl2dhg')and contains(@class,'xggy1nq')and contains(@class,'x1a2a7pz')and contains(@class,'x6s0dn4')and contains(@class,'xjbqb8w') and contains(@class,'x1ejq31n') and contains(@class,'xd10rxx') and contains(@class,'x1sy0etr') and contains(@class,'x17r0tee') and contains(@class,'x1ypdohk') and contains(@class,'x78zum5') and contains(@class,'xl56j7k') and contains(@class,'x1y1aw1k') and contains(@class,'x1sxyh0') and contains(@class,'xwib8y2') and contains(@class,'xurb0ha')]"))).click()
            time.sleep(2)
            # driver.find_element(By.XPATH,"//span/button[contains(@class,'_abl-') and contains(@type,'button')]").click()
            # time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {str(e)}")    

# Wait for the login process to complete (you can use a specific condition here)
# WebDriverWait(driver, 20).until(EC.url_contains('/accounts/login/'))

# Perform actions on Instagram after logging in
# Example: Like a post
# first_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_9AhH0']")))
# first_post.click()
# like_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='fr66n']/button")))
# like_button.click()

# finally:
    # Close the WebDriver
    # driver.quit()

def stopbot():
    driver = webdriver.Chrome()
    driver.quit()
    print('hello, i stopped the bot')
            
startbotbutton = tk.Button(win,text="Start Bot",command=startBot,bg="white",font="Poppins 10 bold",width=8,fg="black",cursor="arrow")
startbotbutton.place(relx=0.2,rely=0.9)
stopbotbutton = tk.Button(win,text="Stop Bot",command=stopbot,bg="red",font="Poppins 10 bold",width=8,fg="black",cursor="arrow")
stopbotbutton.place(relx=0.6,rely=0.9)
win.mainloop()