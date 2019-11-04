# Pages to scrape
URL = ['https://zacatrus.es/juegos-de-mesa.html?cat=10',
      'https://zacatrus.es/juegos-de-mesa.html?cat=12',
      'https://zacatrus.es/juegos-de-mesa.html?cat=92',
      'https://zacatrus.es/juegos-de-mesa.html?cat=130',
      'https://zacatrus.es/juegos-de-mesa.html?cat=137',
      'https://zacatrus.es/juegos-de-mesa.html?cat=138',
      'https://zacatrus.es/juegos-de-mesa.html?cat=139'
      ]

'''
MAIN
'''

from functions import zacatrus_crawler

i = 0
for page in URL:
        
        # Start the crawl spider
        print("Starting to crawl:", page)
        zacatrus_crawler(page, 'https://zacatrus.es/', 1, i)
        i += 1