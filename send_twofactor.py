from selenium import webdriver
from sys import  exit
from time import sleep
from selenium.webdriver.common.by import By
from pub_funcs import saveLogs, saveErrorLogs
from pub_objs import paths
from db_funcs import execute_commit,execute_fetchall

def send_twofactor_password(browser:webdriver.Chrome):

    mypath=paths()
    X_account_username=mypath.username
    twofactorXpath_input=mypath.twofactor_input
    twofactorXpath_btn=mypath.twofactor_btn
    counter=0

    while (counter <= 2):        
        try :
            findTwofactorXpath_input=browser.find_element(By.XPATH, twofactorXpath_input)
            logs='Check your mails and sending your twofactor password less than 2 minuts later'
            saveErrorLogs(logs)
            saveLogs(logs)
        except:
            if counter >= 1 : #it mean we sent a right pass
                sqlQuery ='update your_twofactor_table set used=1, confirmation=1 WHERE twofactor_pass=%s'
                sqlValues=(twofactor_pass,)
                execute_commit(sqlQuery,sqlValues)
                saveErrorLogs('Two-Factor password passed successfully')
                saveLogs('Two-Factor password passed successfully')
            return   
        sleep(100)
        sqlQuery ='select twofactor_pass from your_twofactor_table where login_username_info=%s order by id desc limit 1;'
        sqlValues=(X_account_username,)
        lasttwofactor_result=execute_fetchall(sqlQuery,sqlValues)

        if lasttwofactor_result:
            twofactor_pass=lasttwofactor_result[0]
        elif not lasttwofactor_result:
            saveErrorLogs('your_twofactor_table is empty - XCrawler will off')
            saveLogs('your_twofactor_table is empty - XCrawler will off')
            exit() 
        findTwofactorXpath_input.clear()
        findTwofactorXpath_input.send_keys(twofactor_pass)
        sleep(2)
        findNextBtn=browser.find_element(By.XPATH, twofactorXpath_btn)
        clickNextBtn=findNextBtn.click()

        if counter==0:
            sleep(5)
            try:
                findNextBtn
                saveErrorLogs('Incorrect Two-Factor password - send a new Two-Factor password less than 2 minutes later')
                saveLogs('Incorrect Two-Factor password - send a new Two-Factor password less than 2 minutes later')
            except:
                sqlQuery ='update your_twofactor_table set used=1, confirmation=1 WHERE twofactor_pass=%s'
                sqlValues=(twofactor_pass,)
                execute_commit(sqlQuery,sqlValues)
                saveErrorLogs('Two-Factor password passed successfully')
                saveLogs('Two-Factor password passed successfully')
                return       

        counter += 1

    saveErrorLogs('Incorrect Two-Factor password for second time - XCrawler will off')
    saveLogs('Incorrect Two-Factor password for second time- XCrawler will off')
    exit()