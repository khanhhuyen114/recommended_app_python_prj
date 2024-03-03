import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


def save_cookie(email, password):
    # Declare the browser
    browser = webdriver.Chrome(service=Service("./chromedriver.exe"))

    # Open faceboook
    browser.get('http://facebook.com')

    # Login
    # find email box and password box by its ID
    txtUser = browser.find_element(By.ID, "email")
    txtUser.send_keys(email)

    txtPassword = browser.find_element(By.ID, "pass")
    txtPassword.send_keys(password)

    txtPassword.send_keys(Keys.ENTER)

    sleep(10)
    # 3. Save cookie to file my_cookie.pkl after login
    pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb"))

    # 4. Close browser
    browser.close()
