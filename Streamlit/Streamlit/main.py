import streamlit as st
from openpyxl import load_workbook
import Game
import pandas as pd
import folium
from streamlit_folium import st_folium
import random as rd
import time
import datetime
import requests
from streamlit_lottie import st_lottie


#get animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
#Load animation
spaceship = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_e16yAs.json")
coding = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_wqypnpu5.json")
gamers = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_sdsq6yiq.json")
watchmovie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
sad1 = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_hfnjm1i3.json")
sad2 = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t9nbbl1t.json")

# -----------Set up data
    #--------Game--------
wb = load_workbook(r'data1/DataFrame.xlsx')
ws = wb.active
game_name = Game.take_name_game()
game_key = [0]
    # tao cac bien rieng cho tung lua chon cua game
for i in range(1,len(game_name)):
    game_key.append(Game.game_choice(game_name[i]))
    #nhap du lieu cua data vao cac bien
for i in range(1,len(game_key)-1):
    game_key[i].add_infor()
# Load animation

    #--------Film-----------
df_film = pd.read_csv("data1/film.csv")

# -------Event-----------

df_event = pd.read_csv("data1/events.csv")
df_event.pop("Unnamed: 0")



# ------------------------------HAM TRONG WEB-----------------------------------------

###### Phan GAME

        # -----------ham hien ra map-----------
def display_map(id):
    """hien ra map va vi tri cua dia diem dc danh gia la tot nhat cua tro choi do"""
    map = folium.Map(location=[21.027763, 105.834160],zoom_start= 14)
    folium.Marker(location=[game_key[id].lattitude,game_key[id].longtitude],tooltip=f'{game_name[id]}',popup=f'{game_key[id].name_place}').add_to(map)
    st_folium(map, width=1400, height=450)
# Ham random
def random_things(a):
    """ham random 1 tro choi va se giu nguyen tro choi do cho den khi an vao nut shuffle"""
    # initializing with a random number
    if "rn" not in st.session_state:
        st.session_state["rn"] = rd.choice(a)
    # callback function to change the random number stored in state
    def change_number():
        st.session_state["rn"] = rd.choice(a)
        return
    ## button to generate a new random game
    col1, col2 = st.columns(2)
    with col1:
        st.header(f'Ha Noi {endpoint} {emoji[3]}')
        st.button("Shuffle", on_click=change_number)
        with st.spinner('Wait a moment.....'):
            time.sleep(2)
        st.success(st.session_state.rn)
    with col2:
        st_lottie(gamers, height=200, key="gamers")
def option_for_chart(i):
    """hien ra 10 ket qua tuy theo cac option cua ng dung"""
    st.write('-' *50)
    fr = pd.DataFrame.from_dict(game_key[i].infor)
    st.header('More place...')
    options = st.selectbox(
        'More options for sorting',
        ['Number of rating','Rating','Both'],
    )
    if options == 'Number of rating':
        a1 = fr.sort_values(by='Number_of_rating', ascending=False)
        st.table(a1[:10])
    elif options == 'Rating':
        a2 = fr.sort_values(by='Rating', ascending=False)
        st.table(a2[:10])
    else:
        a3 = fr.sort_values(by=['Number_of_rating','Rating'],ascending=False)
        st.table(a3[:10])

def best_choice(i):
    '''Hien ra ket qua tot nhat'''
    st.write('This is the best place for this game')
    display_map(i)
    best_choice = game_key[i].take_best_choice()
    st.table(best_choice)

def choose_filter_for_random_game_choice(i):
    """Random 1 place based on lua chon cua nguoi dung"""
    fr = pd.DataFrame.from_dict(game_key[i].infor)
    st.write('-' * 50)
    col1, col2 = st.columns([1,3])
    with col1:
        st.header('Filter'+emoji[1])
        rate1 = st.selectbox(
            'Rating is higher than',
            (2.0,3.0,4.0),
        )
        number_of_rating1 = st.selectbox(
            'Number of rating is higher than',
            (10,50,100,300,500,700,1000)
        )
        time_open = st.selectbox(
            'Choose range time opening',
            ['8:00 - 12:00', '12:00 - 18:00', '18:00- 24:00']
        )
        df_selection = fr.query(
            'Rating >= @rate1 and Number_of_rating >= @number_of_rating1'
        )
    if df_selection.empty:
        st.error("Sorry, there's no games matched your selection" +emoji[2])
        st_lottie(sad2, height=200, key="sad2")
    else:
        df_selection = df_selection.sample()
        with col2:
            st.header('Another Place' +emoji[7])
            # display picture
            st.image(game_key[i].picture[0])
        st.table(df_selection)




##  ----------------------MAIN PAGE ----------------------------------


emoji = ['🏃','🧧','😢','🕹️','🎭','🎬','📝','🏠']
st.title('ĐI CHƠI ĐÂU ' + emoji[0] + '?')
# phan side bar

st.sidebar.header('Welcome to Di choi dau team web'+ emoji[0])
endpoint = st.sidebar.selectbox("Choice", ['Game', 'Event','Film'])
st.sidebar.write("Some sidebar text")

# noi dung chinh
if endpoint == 'Game':
    random_things(game_name)
    id = game_name.index(st.session_state.rn)
    best_choice(id)
    choose_filter_for_random_game_choice(id)
    option_for_chart(id)


if endpoint == 'Film':
    col1, col2 = st.columns(2)
    with col1:
        st.header(f'Ha Noi {endpoint} {emoji[5]}')
    st.write("---")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header("You can grab a movie for your leisure time here ><")
        with col2:
            st_lottie(watchmovie, height=200, key="watchmovie")


    st.write("---")
    with st.container():
        col1, col2 = st.columns(2)
        film_picked = {
            "Name": [],
            "Genre": [],
            "Release date": [],
            "Play Time": [],
            "Poster URL": [],
            "View grade": []
        }
        reday = st.date_input("After which day that you are able to watch movie?", datetime.date(2022, 11, 9))
        max = len(df_film)
        count = -1
        try:
            for i in range(0, max):
                if str(reday) >= str(df_film["Release date"][i]):
                    film_picked["Name"].append(df_film["Name"][i])
                    film_picked["Genre"].append(df_film["Genre"][i])
                    film_picked["Release date"].append(df_film["Release date"][i])
                    film_picked["Play Time"].append(df_film["Play Time"][i])
                    film_picked["Poster URL"].append(df_film["Poster URL"][i])
                    film_picked["View grade"].append(df_film["View grade"][i])
                    count += 1
            df_film_picked = pd.DataFrame.from_dict(film_picked)
            max = count

            if st.button('Random another one'):
                rd = rd.randint(0, max)
                with col1:
                    st.image(df_film_picked["Poster URL"][rd], width=250)
                with col2:
                    st.subheader("Movie name: " + df_film_picked["Name"][rd])
                    st.subheader("Genre: " + df_film_picked["Genre"][rd])
                    st.subheader("Release date(yyyy/mm/dd): " + df_film_picked["Release date"][rd])
                    st.subheader("Play time: " + df_film_picked["Play Time"][rd])
                    st.subheader("View grade: " + str(df_film_picked["View grade"][rd]))
            else:
                with col1:
                    st.image(df_film_picked["Poster URL"][0], width=250)
                with col2:
                    st.subheader("Movie name: " + df_film_picked["Name"][0])
                    st.subheader("Genre: " + df_film_picked["Genre"][0])
                    st.subheader("Release date(yyyy/mm/dd): " + df_film_picked["Release date"][0])
                    st.subheader("Play time: " + df_film_picked["Play Time"][0])
                    st.subheader("View grade: " + str(df_film_picked["View grade"][0]))
        except:
            st_lottie(sad1, height=200, key="sad1")
            st.error("There 's no appropriate film based on your choice")

if endpoint == 'Event':
    col1, col2 = st.columns(2)
    with col1:
        st.header(f'Ha Noi {endpoint} {emoji[4]}')
    with st.container():
        st.write("---")
        st.header("You can also pick a specified day too!")
        st.write("##")
        day_picked = st.date_input("Which day that you want to join an event?",  datetime.date(2022, 11, 9))
        event_picked = {
            "Name": [],
            "Location":[],
            "Y/M/D": [],
            "Start_hour": []
        }
        for i in range(0, len(df_event)):
            if str(day_picked) == str(df_event["Y/M/D"][i]):
                event_picked["Name"].append(df_event["Name"][i])
                event_picked["Location"].append(df_event["Location"][i])
                event_picked["Y/M/D"].append(df_event["Y/M/D"][i])
                event_picked["Start_hour"].append(df_event["Start_hour"][i])

        df_event_picked = pd.DataFrame.from_dict(event_picked)
        st.dataframe(event_picked, use_container_width=True)

    with st.container():

        col1, col2 = st.columns(2)
        with col1:
            st.write("####")
            st.write(
                """
                The table of events have been collected.
                You can sort information in each column by clicking the header "Name"/"Location"/"Y/M/D"/Start_hour/
                and see the whole table just by clicking the symbol on the upper right of the table 
                (or scroll :v)
                """
            )

        with col2:
            st_lottie(spaceship, height=200, key="spaceship")

    st.dataframe(df_event, None, 500)

#homthu
with st.container():
    st.write("---")
    st.write("##")

contact_form = """
<form action="https://formsubmit.co/dichoidaudi@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="email" name="email" placeholder="Your email" required>
    <textarea name="message" placeholder="Your message here" required></textarea>
    <button type="submit">Send</button>
</form>
"""


leftcol, rightcol = st.columns(2)
with leftcol:
    st.header("Some suggestion to help our web better" + emoji[6])
    st.write("##")
    st.markdown(contact_form, unsafe_allow_html=True)
with rightcol:
    st_lottie(coding, height=350, key="code")

