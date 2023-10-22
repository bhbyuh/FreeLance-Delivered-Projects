from selenium import webdriver
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np

Numbers=pd.read_csv('MC data1.csv')
Numbers=list(Numbers['Numbers'])
Total_len=len(Numbers)

Number=[]
Name=[]
phone=[]
Entity_Type=[]
Power_units=[]

url='https://safer.fmcsa.dot.gov/CompanySnapshot.aspx'

driver=webdriver.Chrome()

current=0
while(current<Total_len):
    driver.get(url)
    File_data_Number=Numbers[current]
    ELEM=driver.find_elements(By.NAME,'query_param')
    ELEM[1].click()
    ELEM=driver.find_element(By.NAME,'query_string').send_keys(File_data_Number)
    td_elements = driver.find_elements(By.TAG_NAME, 'td')
    search_button = driver.find_element(By.XPATH, "//input[@type='SUBMIT' and @value='Search']")
    search_button.click()
    time.sleep(2)
    data=driver.page_source
    data=BeautifulSoup(data,'html.parser')
    Elements=data.find_all('tbody')
    Elements=data.find_all('td',{'class':'queryfield'})
    if(len(Elements)!=0):
        if(Elements[0].text!=np.nan):
            Entity_Type.append(Elements[0].text)
        else:
            Entity_Type.append("")
        if(Elements[3].text!=np.nan):
            Name.append(Elements[3].text)
        else:
            Name.append("")
        if(Elements[6].text!=np.nan):
            phone.append(Elements[6].text)
        else:
            phone.append("")
        if(Elements[12].text!=np.nan):
            Power_units.append(Elements[12].text)
        else:
            Power_units.append("")
        Number.append(File_data_Number)
    current+=1
    Elements=np.nan

df=pd.DataFrame({"Numbers":Number,"Name":Name,"phone_Number":phone,"EntityType":Entity_Type,"Powerunits":Power_units})
df.to_csv('CD_Output.csv')

driver.quit()