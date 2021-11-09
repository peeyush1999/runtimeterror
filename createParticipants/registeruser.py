import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
#import pyautogui
import random
import xlrd
import sys
import string
import random



data = xlrd.open_workbook('password.xls')
table = data.sheet_by_name(u'Sheet1')

userId="" #input-4
password=""#input-5


def processdata():
    table = data.sheet_by_name(u'Sheet2')
    #driver = webdriver.Chrome(executable_path=r'webdrivers/chromedriver.exe')
        #/home/peeyushsahu/Desktop/DownloadSubmission

    
    #driver.maximize_window()



    



    
    
    for row in range(30):
        
        driver = webdriver.Firefox(executable_path=r'webdrivers/geckodriver');
        driver.get("http://127.0.0.1:5000/")
        driver.execute_script("toggle()")
        
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
        email = name+"@"+"gmail.com"
        password="qwerty"
        college = "IIITH"
        print(name,password)
        driver.find_element_by_name('Name').send_keys(name)        
        driver.find_element_by_name('Email').send_keys(email)
        driver.find_element_by_name('Password').send_keys(password)
        driver.find_element_by_name('College').send_keys(college)
        driver.find_element_by_name('type').send_keys("participant")
        #driver.find_element_by_id('Email').send_keys(name)
        driver.find_element_by_id('Password').send_keys(password)

        time.sleep(1)
        driver.find_element_by_id('register').click()

        
                
        

    driver.quit()        
        

processdata()

#=====================================================


print("Completed!!!!")


  
