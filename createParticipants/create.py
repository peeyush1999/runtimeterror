import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
#import pyautogui
import random
import xlrd
import sys



data = xlrd.open_workbook('password.xls')
table = data.sheet_by_name(u'Sheet1')

userId="" #input-4
password=""#input-5


def processdata():
    table = data.sheet_by_name(u'Sheet2')
    #driver = webdriver.Chrome(executable_path=r'webdrivers/chromedriver.exe')
        #/home/peeyushsahu/Desktop/DownloadSubmission

    
    #driver.maximize_window()



    



    
    
    for row in range(table.nrows):
        
        driver = webdriver.Firefox(executable_path=r'webdrivers/geckodriver');
        driver.get("http://127.0.0.1:5000/")
        
        name = str(table.cell(row,0).value)
        password=str(table.cell(row,1).value)
        print(name,password)
        
        driver.find_element_by_id('LEmail').send_keys(name)
        driver.find_element_by_id('LPassword').send_keys(password)
        time.sleep(2)
        driver.find_element_by_id('Login').click()

        
                
        

    #driver.quit()        
        

processdata()

#=====================================================


print("Completed!!!!")


  
