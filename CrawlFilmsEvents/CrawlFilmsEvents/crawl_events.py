from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import datetime
import pickle
from time import sleep
from scroll import scroll_fb
driver = webdriver.Chrome(service=Service("./chromedriver.exe"))

events = dict()
events['Name'] = []
events['Location'] = []
events['Y/M/D'] = []
events['Start_hour'] = []


"""Function to add last filtered list to dictionary "events" """


def final_list_event(after_filter: list):
    for i in after_filter:
        if i[1] not in events:
            events['Name'].append(i[1])
            events['Location'].append(i[2])
            events['Y/M/D'].append(i[0][0])
            try:
                events['Start_hour'].append(i[0][1])
            except:
                events['Start_hour'].append('All day')
        else:
            continue


"""CONVERT TIME TO FORMAT"""


def convert_time_gg(strn: str):  # convert with VNese language
    strn: str = strn.replace(' thg ', '/')
    strn: list = strn.split('\n')
    strn[0]: str = strn[0] + '/' + str(datetime.datetime.now().year)
    strn[0] = strn[0][-10::]
    strn[0] = datetime.datetime.strptime(strn[0], "%d/%m/%Y").strftime("%Y-%m-%d")
    return strn


def convert_time_fb(strn):
    """dictionary to save weekday as number with same format as datetime library"""
    weekday: dict = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY', 5: 'SATURDAY', 6: 'SUNDAY'}

    """formatting time with each case"""

    # seperate day and start hour (if the event has)
    strn: list = strn.split(' AT ')

    # if event happend this week
    if strn[0].find('THIS') != -1:
        strn[0] = strn[0].replace('THIS ', '')
        strn[0] = strn[0].replace(strn[0], str(list(weekday.keys())[list(weekday.values()).index(strn[0].upper())]))
        crawl_day: int = datetime.datetime.now().weekday()
        delta: int = int(strn[0]) - crawl_day
        coming_date: datetime = datetime.datetime.now() + datetime.timedelta(days=delta)
        strn[0]: str = coming_date.strftime("%Y-%m-%d")
    # if event just tell that today or tomorrow
    elif strn[0].find('TODAY') != -1:
        strn[0]: str = datetime.datetime.now().strftime("%Y-%m-%d")
    elif strn[0].find('TOMORROW') != -1:
        coming_date: datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        strn[0]: str = coming_date.strftime("%Y-%m-%d")
    # other case with specific day
    else:
        try:
            # try if it has year in its time
            try:
                strn[0]: datetime = datetime.datetime.strptime(strn[0], '%a, %d %b %Y')
            except:
                strn[0]: datetime = datetime.datetime.strptime(strn[0], '%a, %b %d %Y')
            # if not, append year to the end
        except:
            strn[0]: str = strn[0] + str(datetime.datetime.now().year)
            try:
                strn[0]: datetime = datetime.datetime.strptime(strn[0], '%a, %d %b%Y')
            except:
                strn[0]: datetime = datetime.datetime.strptime(strn[0], '%a, %b %d%Y')
            # compare date time after formatting with today, if it is past event, return "-", else return time
        if strn[0] < datetime.datetime.now():
            strn[0]: str = '-'
        else:
            strn[0]: str = strn[0].strftime("%Y-%m-%d")

    return strn


"""GOOGLE"""


def crawl_events_google(browser, link_search):
    # access to search link
    browser.get(link_search)

    # crawl data by xpath
    names: list = browser.find_elements(By.XPATH, "//div[@class = 'bVj5Zb FozYP']")
    locations: list = browser.find_elements(By.XPATH, "//div[@class = 'TCYkdd FozYP']")
    datetimes: list = browser.find_elements(By.XPATH, "//div[@class = 't3gkGd']")
    day_hour = list()

    for i in datetimes:
        # convert date to format
        date_convert = convert_time_gg(i.text)
        # add date to list after formatting
        day_hour.append(date_convert)

    # check if it has start hour or not
    for i in day_hour:
        if len(i) == 1:
            i.append('All day')
        else:
            continue

    # add data to final dictionary
    for i, j in zip(names, locations):
        events['Name'].append(i.text)
        events['Location'].append(j.text)
    for i in day_hour:
        events['Y/M/D'].append(i[0])
        events['Start_hour'].append(i[1])


"""PAGE FACEBOOK"""


def crawl_events_facebook_type_1(browser, link_search):
    # access to search link
    browser.get(link_search)

    # load saved cookies so that no need to log in several times
    cookies = pickle.load(open("my_cookie.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    # load the web again after login
    browser.get(link_search)
    sleep(3)

    try:
        before_filter = list()
        after_filter = list()
        for i in range(5):
            try:  # try to click if it is not show all the events
                button = browser.find_element(By.XPATH, '//div[@aria-label = "See more"]')
                button.click()
                sleep(3)
            except:
                break

        # crawling events information by xpath
        up_coming_events: list = browser.find_elements(By.XPATH, '//div[@class = "x78zum5 xdt5ytf x4cne27 xifccgj"]')

        # formatting time in crawled data
        for i in up_coming_events:
            i = i.text.split('\n')
            before_filter.append(i)
        for i in before_filter:  # remove if it does not have enough information
            if len(i) <= 1:
                before_filter.remove(i)
        for i in before_filter:  # formatting time
            i[0] = convert_time_fb(i[0])
            try:
                a: str = i[2].split(' – ')
                i[2] = a[1]
            except:
                pass
            if i[0][0] != '-':
                after_filter.append(i)
        # add future events information to dictionary
        final_list_event(after_filter)
    except:
        return 0


def crawl_events_facebook_type_2(browser, link_search):
    browser.get(link_search)

    cookies = pickle.load(open("my_cookie.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.get(link_search)
    sleep(3)
    try:
        before_filter = list()
        after_filter = list()
        try:
            scroll_fb(browser, 1)
        except:
            pass
        up_coming_events: list = browser.find_elements(By.XPATH, '//div[@class = "x78zum5 xdt5ytf xz62fqu x16ldp7u"]')

        for i in up_coming_events:
            i = i.text.split('\n')
            before_filter.append(i)
        for i in range(2):  # delete blank line
            before_filter.pop(i)

        middle_filter = list()
        for i in before_filter:
            try:
                i[2]: str = ''.join([i[2], i[3]])
                middle_filter.append([i[0], i[1], i[2]])
            except:
                pass

        for i in middle_filter:
            i[0] = convert_time_fb(i[0])
            if i[0][0] != '-':
                after_filter.append(i)
        final_list_event(after_filter)
    except:
        return 0
