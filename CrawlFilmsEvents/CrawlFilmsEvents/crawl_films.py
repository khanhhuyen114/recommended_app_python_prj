import http.client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import datetime
list_film = dict()
list_film['Name'] = []
list_film['Genre'] = []
list_film['Release date'] = []
list_film['Play Time'] = []
list_film['Poster URL'] = []
list_film['View grade'] = []


def lotte(link):
    # information to request crawl data by api from web
    conn: http.client.HTTPSConnection = http.client.HTTPSConnection(link)
    payload: str = \
        "ParamList=%7B%22MethodName%22%3A%22GetMovies%22%2C%22channelType%22%3A%22HO%22%2C%22osType%22%3A%22Chrome%22%2C%22osVersion%22%3A%22Mozilla%2F5.0%20(Linux%3B%20Android%206.0%3B%20Nexus%205%20Build%2FMRA58N)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F106.0.0.0%20Mobile%20Safari%2F537.36%20Edg%2F106.0.1370.52%22%2C%22multiLanguageID%22%3A%22LL%22%2C%22division%22%3A1%2C%22moviePlayYN%22%3A%22Y%22%2C%22orderType%22%3A%221%22%2C%22blockSize%22%3A100%2C%22pageNo%22%3A1%7D"

    headers: dict = {
        'cookie': "ASP.NET_SessionId=vdi55enkc3nyspxj25ev3r5q",
        'Content-Type': "application/x-www-form-urlencoded"
        }

    conn.request("POST", "/LCWS/Movie/MovieData.aspx?nocashe=0.3753020082283718", payload, headers)

    res: http.client.HTTPSConnection.getresponse = conn.getresponse()
    data: bytes = res.read()
    film: str = data.decode("utf-8")
    film = film.replace('null', '0')
    film: dict = eval(film)

    for i in film['Movies']['Items']:
        if i['MovieName'].upper() not in list_film['Name']:
            list_film['Name'].append(i['MovieName'])
            list_film['Poster URL'].append(i['PosterURL'])
            list_film['View grade'].append(i['ViewGradeCode'])
            i['ReleaseDate'] = datetime.datetime.strptime(i['ReleaseDate'], "%Y%m%d")
            list_film['Release date'].append(i['ReleaseDate'].strftime('%Y-%m-%d'))
            list_film['Play Time'].append(i['PlayTime'] + ' phút')
            list_film['Genre'].append(i['MovieGenreName'])
        else:
            continue


def cgv(link_search):
    browser: webdriver = webdriver.Chrome(service=Service("./chromedriver.exe"))
    browser.get(link_search)
    sleep(5)
    up_coming_events: list = browser.find_elements(By.CLASS_NAME, "product-info")
    imgs: list = browser.find_elements(By.TAG_NAME, 'img')
    list_img = list()
    for i in imgs:
        i = i.get_attribute('src')
        if i.find('product') != -1:
            list_img.append(i)
    for i in up_coming_events:
        index = up_coming_events.index(i)
        i = i.text.replace('Thể loại: ', ' ')
        i = i.replace('Thời lượng: ', ' ')
        i = i.replace('Khởi chiếu: ', ' ')
        i = i.split('\n')
        if i[0].upper() not in list_film['Name']:
            list_film['Name'].append(i[0])
            list_film['Genre'].append(i[1])
            list_film['Play Time'].append(i[2])
            list_film['Poster URL'].append(list_img[index])
            i[3] = i[3].replace(' ', '')
            date = datetime.datetime.strptime(i[3], '%d-%m-%Y').strftime('%Y-%m-%d')
            list_film['Release date'].append(date)
            list_film['View grade'].append('0')
        else:
            continue
