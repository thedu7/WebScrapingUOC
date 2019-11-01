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
data = ["Nom", "Autor", "Tematica", "Preu", "Temps de joc", "Dificultat", "Jugadors", "Idioma", "Descripcio", "Edat", "URL"]
dato = ["","","","","","","","","","","","","","","","","","",""]
file = 'Juegos-Zacatrus.csv'
basic_url_zacatrus = 'https://zacatrus.es/'
'''
FUNCTIONS
'''

def parse_page_info(url):
    
    # Create a BeautifulSoup object
    soup_info = BeautifulSoup(url, 'html.parser')
    soup_info.encode("utf-8")
        
    dato[2] = soup_info.find(class_='price').text.strip()
    
    games_infos = soup_info.find(class_='additional-attributes-wrapper table-wrapper')
    games_list_infos = games_infos.find_all('td') 
    
    i = 3
    for info in games_list_infos:
        
        dato[i] = info.text.strip()
        i += 1

    dato[i] = soup_info.find(class_="product attribute description").text.strip()

    
def parse_main_page(html):
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    soup.encode("utf-8")
    
    #create_csv(file, data)
    f = csv.writer(open(file, 'w'))
    f.writerow(data)  
    
    # Pull all text from the BodyText div
    games_list = soup.find(class_='products list items product-items')
    
    # Pull text from all instances of <a> tag within BodyText div
    games_list_items = games_list.find_all('a', {'class':'product-item-link'})
    
    # Create for loop to print out all expositions informations
    for games in games_list_items:
    
        links = games.get('href')
        dato[0] = links
        name = games.text.strip()
        dato[1] = name
        
        #crawl new urls
        zacatrus_crawler(links, basic_url_zacatrus, 2)
        
        data_list = (dato[1],
                     dato[3],
                     dato[6],
                     dato[2],
                     dato[10],
                     dato[12],
                     dato[9],
                     dato[15],
                     dato[8],
                     dato[18],
                     dato[0])

        print(data_list)
        
        f.writerow(data_list)

        
def scrap_web_content(html, ind):
    if html is not None:
        print("OK")
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
    print("Starting to crawl:")
    rp = robot_parser(basic_url)
    download(url, rp, mode)

    
def length_of_last_word(s):
    words = s.split()
    if len(words) == 0:
        return 0
    return len(words[-1])