from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
url='https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=dog&gender=A&agegroup=All&location=&site=&onhold=A&orderby=Name&colnum=4&css=https://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=00g45af54a8rdngo3wm8c3o3b04mqgxlu5tl6p7ci53m8s6byp&recAmount=&detailsInPopup=No&featuredPet=Include&stageID='

flag=0
if(os.path.exists("DogsData.csv")):
    flag=1
    df=pd.read_csv('DogsData.csv')
    PreIDs=list(df['ID'])
    Prename=list(df['Name'])
    Pregender=list(df['Gender'])
    Prebreed=list(df['Breed'])
    Pretime=list(df['Time'])
    Prelocation=list(df['Location'])
    
    
driver=webdriver.Chrome()
driver.get(url)

data=driver.page_source
data=BeautifulSoup(data,'html.parser')

name=[]
Elements=data.find_all('div',{'class':'list-animal-name'})
print(len(Elements))
for i in Elements:
    name.append(i.text)


idN=[]
Elements=data.find_all('div',{'class':'list-animal-id'})
print(len(Elements))
for i in Elements:
    idN.append(i.text)


gender=[]
Elements=data.find_all('div',{'class':'list-animal-sexSN'})
print(len(Elements))
for i in Elements:
    gender.append(i.text)

breed=[]
Elements=data.find_all('div',{'class':'list-animal-breed'})
print(len(Elements))
for i in Elements:
    breed.append(i.text)

time=[]
Elements=data.find_all('div',{'class':'list-animal-age'})
print(len(Elements))
for i in Elements:
    time.append(i.text)
    
location=[]
Elements=data.find_all('div',{'class':'hidden'})
print(len(Elements))
for i in Elements:
    location.append(i.text)

idN = [int(item) for item in idN]

if(flag==1):
    Idslength=len(idN)
    count=0
    while(count<Idslength):
        currentId=idN[count]
        if(currentId in PreIDs):
            del name[count]
            del idN[count]
            del gender[count]
            del breed[count]
            del time[count]
            del location[count]
            Idslength-=1
        else:
            count+=1
    name=name+Prename
    idN=idN+PreIDs
    gender=gender+Pregender
    breed=breed+Prebreed
    time=time+Pretime
    location=location+Prelocation
    
df=pd.DataFrame({"ID":idN,"Name":name,"Gender":gender,"Breed":breed,"Time":time,"Location":location})
df.to_csv('DogsData.csv')
driver.quit()