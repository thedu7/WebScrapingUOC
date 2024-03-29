import urllib.request
import requests
import csv
import urllib.robotparser
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

'''
CONFIG
'''

data = ["Nombre", "Tipo", "Precio", "Temática", "Autores", "Tiempo de juego", "Dificultad", "Num. Jugadores", "Idioma", "Edad", "URL", "Descripción"]
data_games = ['Juegos de Tablero', 'Juegos de Cartas', 'Juegos de Rol', 'Juegos de Wargamers', 'Juegos de Miniaturas', 'Juegos de Dados']
file = 'Juegos-Zacatrus.csv'
basic_url_zacatrus = 'https://zacatrus.es/'

'''
FUNCTIONS
'''

def write_csv(data, csv_mode):
    
    # Create_csv(file, data)
    if csv_mode == 0:
        f = csv.writer(open(file, 'w'))
        f.writerow(data)
    else:
        f = csv.writer(open(file, 'a'))
        f.writerow(data)
        print('Data added in:', file)

def parse_page_info(url):
    
    # Create a BeautifulSoup object
    soup_info = BeautifulSoup(url, 'html.parser')
    soup_info.encode("utf-8")
    
    # Pull all text from the class "additional-attributes-wrapper table-wrapper"
    games_infos = soup_info.find(class_='additional-attributes-wrapper table-wrapper')
    
    # Check all the extracted data
    try:
        data[2] = soup_info.find(class_='price').text.strip()
    except AttributeError:
        data[2] = "Precio NO identificado"
    
    try:
        data[4] = games_infos.find("td", {'data-th':'Autor'}).text.strip()
    except AttributeError:
        data[4] = "Autores NO identificados"
        
    try:
        data[3] = games_infos.find("td", {'data-th':'Temática'}).text.strip()
    except AttributeError:
        data[3] = "Temática NO identificada"
    
    try:
        data[5] = games_infos.find("td", {'data-th':'Tiempo de juego'}).text.strip()
    except AttributeError:
        data[5] = "Tiempo de juego NO identificado"
    
    try:
        data[6] = games_infos.find("td", {'data-th':'Complejidad'}).text.strip()
    except AttributeError:
        data[6] = "Dificultad NO identificada"
        
    try:
        data[7] = games_infos.find("td", {'data-th':'Núm. jugadores'}).text.strip()
    except AttributeError:
        data[7] = "Núm. Jugadores NO identificados"
    
    try:
        data[8] = games_infos.find("td", {'data-th':'Idioma'}).text.strip()
    except AttributeError:
        data[8] = "Idioma NO identificado"
    
    try:
        data[9] = games_infos.find("td", {'data-th':'Edad'}).text.strip()
    except AttributeError:
        data[9] = "Edad NO identificada"
    
    try:
        data[11] = soup_info.find(class_="product attribute description").text.strip()
    except AttributeError:
        data[11] = "No hay descripción"

        
def parse_main_page(html, csv_ind):
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    soup.encode("utf-8")  
    
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
        data[1] = data_games[csv_ind]
        
        # Crawl the new games urls = 'links'
        zacatrus_crawler(links, basic_url_zacatrus, 2, 1)

        # Write data in csv(data)
        write_csv(data, 1)
        
        
def scrap_web_content(html, ind, csv):
    if html is not None:
        if ind == 1:
            parse_main_page(html, csv)    
        else:
            parse_page_info(html)
    else:
        print("Html is empty")
        return
        
        
def download(url, robot_parser, ind, csv, user_agent='uoc_wswp', num_retries=10):
    print('Downloading:', url)
    headers = {'User-Agent': user_agent}
    requests = urllib.request.Request(url, headers = headers)
    try:
        if robot_parser.can_fetch(user_agent, url):
            html = urllib.request.urlopen(requests).read()
            print('Parsing:', url)
            scrap_web_content(html, ind, csv)
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


def zacatrus_crawler(url, basic_url, mode, csv):
    rp = robot_parser(basic_url)
    if csv == 0:
        write_csv(data, csv)
    download(url, rp, mode, csv)
