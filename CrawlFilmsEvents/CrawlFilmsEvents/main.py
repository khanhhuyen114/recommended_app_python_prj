import pandas as pd
from crawl_events import driver
from save_cookie_login_fb import save_cookie

"""Import function from crawl events of facebook and google"""
from crawl_events import crawl_events_facebook_type_1
from crawl_events import crawl_events_facebook_type_2
from crawl_events import crawl_events_google

"""Import function from crawl films of lottecinema and cgv"""
from crawl_films import lotte
from crawl_films import cgv

"""Import dictionary of crawling events and crawling film"""
from crawl_films import list_film
from crawl_events import events

"""Save cookies of facebook for crawling events facebook"""
save_cookie("0383701338", "pythonproject")

"""Crawling data"""

# film
lotte("www.lottecinemavn.com")
cgv('https://www.cgv.vn/default/movies/now-showing.html/')


# google
keywordd = 'Hanoi'
crawl_events_google(driver, 'https://www.google.com/search?q=event ' + keywordd)

# facebook
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/hanoirockcity.welive/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/Goethe.Institut.Hanoi/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/VCCAVIETNAM/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/neuyouthfestival/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/PhilosapiensCircle/events/')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/vanmieuquoctugiam/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/ca.library.vietnam/events')
crawl_events_facebook_type_1(driver, 'https://www.facebook.com/viac.vn/events')

crawl_events_facebook_type_2(driver, 'https://www.facebook.com/vincentlecafehanoi/events')
crawl_events_facebook_type_2(driver, 'https://www.facebook.com/ARCH.cafe.bar.rooftop.Hanoi/events')
crawl_events_facebook_type_2(driver, 'https://www.facebook.com/hoichoxuangiangvo/events')
crawl_events_facebook_type_2(driver, 'https://www.facebook.com/IFVHanoi/events')

"""Close Chrome after crawling"""
driver.close()


"""Export data in dictionary to csv"""
pd.DataFrame.from_dict(events).to_csv('events.csv')
pd.DataFrame.from_dict(list_film).to_csv('film.csv')
