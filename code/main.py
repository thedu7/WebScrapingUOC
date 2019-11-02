'''
MAIN
'''

from functions import zacatrus_crawler

#Start the crawl spider
print("Starting to crawl !")
zacatrus_crawler('https://zacatrus.es/juegos-de-mesa.html', 'https://zacatrus.es/', 1)