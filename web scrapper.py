import requests
from bs4 import BeautifulSoup
import time
import xlsxwriter
URL =input("Enter the Url : ")
base_url = input("Enter Base Url")
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
def scrap(start,stop,i):
    global URL
    workbook = xlsxwriter.Workbook('d:\\scrapper\\page'+str(i)+'.xlsx')
    worksheet = workbook.add_worksheet()
    '''
    worksheet.write('A1', 'Name')
    worksheet.write('B1', 'Telephone')
    worksheet.write('C1', 'Website')
    worksheet.write('D1', 'Address')
    worksheet.write('E1', 'Image')
    worksheet.write('F1', 'Cover Image')'''
    row = 0
    col = 0
    for nav in range(start,stop):
        URL = URL + str(nav)
        page = requests.get(URL, headers=headers)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        #soup.find("input",{"name":"service_area"})["value"] = "India"
        #soup.find("input",class_="range-slider")["value"] = "500"
        name = soup.find_all("div", class_="professionals--item-user")
        for x in name:
            child_url = base_url + x.a['href']
            child_page = requests.get(child_url, headers=headers)
            child_soup = BeautifulSoup(child_page.content, 'html.parser')
            try:
                child_tell = child_soup.find("a", class_="show-user--phone").get('href')
            except:
                child_tell = ''
            try:
                child_web = child_soup.find("a", class_="contact--website").get('href')
            except:
                child_web = ''
            try:
                child_img = child_soup.find("div", class_="user-header--avatar")
            except:
                child_img = ''
            try:
                child_Cover_img = child_soup.find("div", class_="show-user")
            except:
                child_Cover_img = ''
            try:    
                child_name = child_soup.find("div", class_="user-header--public-name").get_text()
            except:
                child_name = ''
            try:
                child_add = (child_soup.find("a", class_="category-city--category").get_text()) + " in " + (child_soup.find("a", class_="category-city--city").get_text())
            except:
                child_add = ''
            print(child_name, child_tell, child_web, child_add, child_img.img['src'], child_Cover_img.img['src'])
            worksheet.write(row, col, child_name) 
            worksheet.write(row, col + 1, child_tell) 
            worksheet.write(row, col + 2, child_web) 
            worksheet.write(row, col + 3, child_add) 
            worksheet.write(row, col + 4, child_img.img['src']) 
            worksheet.write(row, col + 5, child_Cover_img.img['src']) 
            row += 1
    workbook.close()
    print("File Created")
start = 1
stop = 2
i = 1
scrap(start,stop,i)