from time import sleep
import random
"""function to scroll web to the end"""
"""input to the function is the connect to the web and the number of times want to scroll"""
def scroll_fb(driver, loop):
    SCROLL_PAUSE_TIME = 0.5
    start = 0
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            continue
        last_height = new_height
        start += 1
        sleep(random.uniform(5,10))
        if start >= loop:
            break