from os import system
from random import *
from time import sleep
import time
import requests
from bs4 import BeautifulSoup


#Не нашел нормального получения деняк, только так

#TODO асинхронность
def get_money(url, procent: int):
    url = "https://explorer.near.org/accounts/"+url
    response = (requests.get(url))
    soup = (BeautifulSoup(response.text, 'lxml'))
    quotes = (soup.find_all('div', class_='c-CardCellText-eLcwWo ml-auto align-self-center col-md-12 col-auto')[2].get_text())
    quotes = float(quotes[:-1])
    money = quotes-(quotes-procent*0.01*quotes)
    money = round(money,1)
    return (money)