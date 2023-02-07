
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
import logging
import requests
from bs4 import BeautifulSoup
import time
# from requests_html import HTMLSession
import psycopg2

app = Flask(__name__)

# session = HTMLSession()


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/booking')
def get():
    today = str(datetime.today().strftime('%Y-%m-%d'))
    tomorrow = str((datetime.today()+timedelta(1)).strftime('%Y-%m-%d'))
    print(today)
    print(tomorrow)
    url = "https://www.booking.com/searchresults.en-us.html?label=bdot-EYeumiUQdogUQpNovL2RLAS267724714005%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9075946%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YV19IumoQ3O5HnTajxNh2ss&sid=70bc0a30ac52d0c3f062474de1eb5192&aid=376381&ss=Monastir&ssne=Monastir&ssne_untouched=Monastir&efdco=1&lang=en-us&sb=1&src_elem=sb&dest_id=-728914&dest_type=city&checkin="+today+"&checkout="+tomorrow+"&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=price"

    target="Marina"
    soup = fetch_current_booking_page(url,target)
    reservation_type="same_day_reservation"
    save_to_database(soup,reservation_type)
    return "TEST"






def save_to_database(soup,reservation_type):
    conn = psycopg2.connect(
      database = "egqfhjwp",
      user = "egqfhjwp",
      host = "manny.db.elephantsql.com",
      port = "5432",
      password = "HJ2OBvd9I0p1N9ZODbYvFX2NWPBSVfUf"
    )
    conn.autocommit = True
    print(soup[0])
    soup[0]= soup[0][0:20]
    print(soup[0])
    cursor = conn.cursor()
    # query = '''INSERT INTO BOOKING_HISTORY(hotel_name,hotel_price) VALUES (' '''+soup[0]+''' ',' ''' +str(soup[1]) + ''' ') '''
    query = "INSERT INTO BOOKING_HISTORY(hotel_name,hotel_price, reservation_type) VALUES ('%s','%s','%s')" % (soup[0],str(soup[1]),reservation_type)
    print(query)
    cursor.execute(query)
    conn.commit()
    print("record inserted")
    conn.close()
    return "ok"


def fetch_current_booking_page(url,target):
  #logging.info('fetching current url: '+ url)
  page = requests.get(url)
  soup =BeautifulSoup(page.content,'html.parser')
  card_list = find_cards(soup)
  #   save_test_files(soup,card_list)
  for card_elem in card_list:
        hotel_name = get_hotel_name(card_elem)
        hotel_price =get_hotel_price(card_elem)
        if target in hotel_name:
            # logging.info('found value of hotel with name: '+ hotel_name)
            # logging.info('the price of the hotel is: '+ hotel_price)
            return [hotel_name,hotel_price]
        else:
            #logging.info('unfortunately the hotel you want is not found')
            return ["hotel not found","0"]

def get_hotel_name(card_elem):
    result = card_elem.findAll('span',class_='bui-card__title')
    # print(result[0].text)
    try:
        return result[0].text
    except:
        return "not found name"

def get_hotel_price(card_elem):
    result = card_elem.findAll('div',class_='bui-price-display__value bui-f-color-constructive')
    # print(result[0].text)
    try:
        return result[0].text
    except:
        return "not found price"

def find_cards(soup):
    card_list = []
    for card in soup.findAll('div',class_='sr__card js-sr-card'):
        card_list.append(card)
    return card_list


def save_test_files(soup,card_list):
    with open("fetched_page.html","w", encoding='utf-8') as fetched:
        fetched.write(str(soup.prettify()))
    with open("output2.html","w",encoding='utf-8') as file:
        file.write(str(card_list[0].prettify()))
    file.close()
    fetched.close()