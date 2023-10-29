from selenium.webdriver.common.keys import Keys 
from selenium import webdriver
from bs4 import BeautifulSoup
import os, send_twofactor
from time import sleep
from selenium.webdriver.common.by import By
import datetime
from sys import exit
from pub_objs import paths
from pub_funcs import saveLogs, saveErrorLogs,connect,savePID
from sys import  exit
from selenium.webdriver.chrome.options import Options
from db_funcs import execute_commit,execute_fetchall

def scraping_x():
    realPID = os.getpid()
    savePID(realPID,"real")
    databaseObject = paths()

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )
    browser = webdriver.Chrome(chrome_options=option, executable_path=routs.browserRoute)

    browser_PID = browser.service.process.pid
    savePID(browser_PID,"browser")

    # browser.maximize_window()
    browser.set_window_size(1200,800)
    login(browser)
    while True:
        connect()
        # go to main page 
        browser.get('https://x.com/home')
        sleep(20)
        for scroll in range(10):
            connect()
            browser.execute_script("window.scrollTo(0, window.scrollY + 800)")
            sleep(2)

        sleep(2)
        pageSource_html = browser.page_source
        soup = BeautifulSoup(pageSource_html, "html.parser")
        posts = soup.find_all(class_ = databaseObject.post_path)
        posts_loop(posts)
        saveLogs('standby mode for 1 hour')
        sleep(3600)             
        saveLogs('standby mode finished after 1 hour, refresh x home page')     

def login(selenium_driver:webdriver.Chrome):
    databaseObject = paths()
    browser=selenium_driver
    username_string = databaseObject.username
    password_string = databaseObject.password
    connect()
    browser.get(databaseObject.login_link)
    sleep(20)
    connect()
    try:    
        elementID = browser.find_element(By.XPATH,'//*[@id="layers"]'+databaseObject.username_input)
        elementID.send_keys(username_string)
    except:
        saveErrorLogs('not valid path for username_input or username_string, check and run again')
        saveLogs('not valid path for username_input or username_string, check and run again')
        exit()
    connect()
    sleep(10)
    try:
        browser.find_element(By.XPATH, databaseObject.next_button_path).click() #next btn
    except:    
        saveErrorLogs('not valid path for next_button_path, check and run again')
        saveLogs('not valid path for next_button_path, check and run again')
        exit()    
    connect()
    sleep(5)
    try:
        elementID = browser.find_element(By.XPATH, '//*[@id="layers"]'+databaseObject.password_input)
        elementID.send_keys(password_string)
    except:    
        saveErrorLogs('not valid path for password_input or password_string, check and run again')
        saveLogs('not valid path for password_input or password_string, check and run again')
        exit()      
    sleep(5)
    connect()
    try:
        browser.find_element(By.XPATH, '//*[@id="layers"]'+databaseObject.login_path).click() #next btn
    except:    
        saveErrorLogs('not valid path for login_path button, check and run again')
        saveLogs('not valid path for login_path button, check and run again')
        exit()      
    sleep(20)
    connect()
    send_twofactor.send_twofactor_password(browser)     
    return

def posts_loop(posts_inpage):
    posts=posts_inpage
    databaseObject = paths()
    for post in posts:
        post:BeautifulSoup
        find_link = post.find(class_ = databaseObject.post_link_path)
        if find_link:
            aTag = find_link.find('a')
            if aTag:
                href_aTag = aTag['href']
                post_Link = "www.x.com" + href_aTag
            else:
                saveErrorLogs('user ID path need to be update, check and run again')
                saveLogs('user ID path need to be update, check and run again')
                exit()          
        elif not find_link:
            break

        sqlquery='SELECT post_Link FROM x_message'
        all_postLinks:list=execute_fetchall(sqlquery)

        if post_Link not in all_postLinks:

            sleep(2)
            date = datetime.datetime.utcnow()
            utc_time = str(date.timestamp())
            row_id = str(utc_time.replace(".", ""))
            if row_id.__len__() <= 15 : 
                differenceOfTwoNumbers = 16 - row_id.__len__()
                row_id = row_id + ('0'* differenceOfTwoNumbers)
            date = str(date)

            find_author = post.find(class_=databaseObject.author_path)
            if find_author:
                author = find_author.get_text()
            else: 
                author='undefined'
                saveErrorLogs('author path need to be update')
                saveLogs('author path need to be update')
            sleep(1)

            find_userid = post.find(class_ = databaseObject.id_path)
            if find_userid:
                userid = find_userid.get_text()
            else: 
                userid='undefined' 
                saveErrorLogs('user ID path need to be update')
                saveLogs('user ID path need to be update')
            sleep(1)

            find_postDate = post.find(class_ = databaseObject.date_path)
            if find_postDate:
                postDate = find_postDate.get_text()
            else: 
                postDate='undefined' 
                saveErrorLogs('post date path need to be update')
                saveLogs('post date path need to be update')
            sleep(1)

            find_description = post.find(class_ = databaseObject.text_path)
            if find_description:
                description = find_description.get_text()
            else:
                description='undefined'
                saveErrorLogs('post date path need to be update')
                saveLogs('post date path need to be update')
            sleep(1)

            arraymedia=[]
            find_images = post.find('img')
            if find_images:
                for image in find_images:
                    if "media" in image['src'] :
                        media= image['src']
                        arraymedia.append(media) 

            mystring="@"
            mystring = mystring.join(arraymedia)
            arraymedia =  mystring
            if arraymedia == "":
                arraymedia =='undefined'
            
            now = str(datetime.datetime.now())

            isvideo = post.find(class_ = databaseObject.video_path)
            if isvideo:
                video="1"
            else:
                video="0"

            if post.find(class_ = databaseObject.retweeted_path):
                Retweetedstatus="1"
                Retweetedname= post.find(class_ = databaseObject.retweetedname_path)
                if "Pinned Tweet" in Retweetedname:
                    Retweetedid =='undefined' 
                    Retweetedname =='undefined'                   
                else:
                    Retweetedid= post.find(class_ = databaseObject.retweetedid_path)
                    Retweetedid = Retweetedid['href']     
                sleep(2)
            else:
                Retweetedstatus="0"
                Retweetedname='undefined'
                Retweetedid='undefined'                
                sleep(2)   

            sqlquery="INSERT INTO your_x_message (row_id,author_EachPost,id_EachPost,text_EachPost,media_Link,post_Link,Retweeted_status,Retweeted_name,Retweeted_id,is_video,local_time,u_time,post_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            sqlvals=(row_id,author,userid,description,arraymedia,post_Link,Retweetedstatus,Retweetedname,Retweetedid,video,now,date,postDate,)
            execute_commit(sqlquery,sqlvals)
        
    return



scraping_x()