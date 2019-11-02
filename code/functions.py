import urllib.request
import requests
import csv
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import time
from bs4 import BeautifulSoup

'''
CONFIG
'''

data = ["Nom", "Autors", "Temàtica", "Preu", "Temps de joc", "Dificultat", "Num. Jugadors", "Idioma", "Descripció", "Edat", "URL"]
file = 'Juegos-Zacatrus.csv'
basic_url_zacatrus = 'https://zacatrus.es/'

'''
FUNCTIONS
'''

def parse_page_info(url):
    
    # Create a BeautifulSoup object
    soup_info = BeautifulSoup(url, 'html.parser')
    soup_info.encode("utf-8")
    
    # Pull all text from the class "additional-attributes-wrapper table-wrapper"
    games_infos = soup_info.find(class_='additional-attributes-wrapper table-wrapper')
    
    # Check all the extracted data
    try:
        data[3] = soup_info.find(class_='price').text.strip()
    except AttributeError:
        data[3] = "Preu NO identificat"
    
    try:
        data[1] = games_infos.find("td", {'data-th':'Autor'}).text.strip()
    except AttributeError:
        data[1] = "Autors NO identificat/s"
        
    try:
        data[2] = games_infos.find("td", {'data-th':'Temática'}).text.strip()
    except AttributeError:
        data[2] = "Temàtica NO identificada"
    
    try:
        data[4] = games_infos.find("td", {'data-th':'Tiempo de juego'}).text.strip()
    except AttributeError:
        data[4] = "Temps de joc NO identificat"
    
    try:
        data[5] = games_infos.find("td", {'data-th':'Complejidad'}).text.strip()
    except AttributeError:
        data[5] = "Dificultat NO identificada"
        
    try:
        data[6] = games_infos.find("td", {'data-th':'Núm. jugadores'}).text.strip()
    except AttributeError:
        data[6] = "Num. Jugadors NO identificat"
    
    try:
        data[7] = games_infos.find("td", {'data-th':'Idioma'}).text.strip()
    except AttributeError:
        data[7] = "Idioma NO identificat"
    
    try:
        data[9] = games_infos.find("td", {'data-th':'Edad'}).text.strip()
    except AttributeError:
        data[9] = "Edat NO identificada"
    
    try:
        data[8] = soup_info.find(class_="product attribute description").text.strip()
    except AttributeError:
        data[8] = "No hi ha descripció"

        
def parse_main_page(html):
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    soup.encode("utf-8")
    
    # Create_csv(file, data)
    f = csv.writer(open(file, 'w'))
    f.writerow(data)  
    
    # Pull all text from the class 'products list items product-items'
    games_list = soup.find(class_='products list items product-items')

    # Pull text from all instances of <a> tag within the class 'product-item-link'
    games_list_items = games_list.find_all('a', {'class':'product-item-link'})
    
    # Create for loop to print out all games informations
    for games in games_list_items:
    
        links = games.get('href')
        data[10] = links
        name = games.text.strip()
        data[0] = name
        
        # Crawl the new games urls = 'links'
        zacatrus_crawler(links, basic_url_zacatrus, 2)
        
        # Write data in csv(data)
        f.writerow(data)
        print('Data added in:', file)
        
        
def scrap_web_content(html, ind):
    if html is not None:
        if ind == 1:
            parse_main_page(html)    
        else:
            parse_page_info(html)
    else:
        print("Html is empty")
        return
        
        
def download(url, robot_parser, ind, user_agent='uoc_wswp', num_retries=10):
    print('Downloading:', url)
    headers = {'User-Agent': user_agent}
    requests = urllib.request.Request(url, headers = headers)
    try:
        if robot_parser.can_fetch(user_agent, url):
            html = urllib.request.urlopen(requests).read()
            print('Parsing:', url)
            scrap_web_content(html, ind)
        else:
            print('Url blocked by robots.txt')
    except urllib.request.URLError as e:
        print('Download error:', e.reason)
        html = none
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_retries-1)
    return


def robot_parser(url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(url, "robots.txt"))
    rp.read()
    return rp


def zacatrus_crawler(url, basic_url, mode):
    rp = robot_parser(basic_url)
    download(url, rp, mode)
