import requests
from bs4 import BeautifulSoup
from urllib import request, parse
#from bs4 import BeautifulSoup
#quote_page = input("Ingresa la pagina web:")

page = requests.post('https://enlinea.sunedu.gob.pe/programa')

soup = BeautifulSoup(page.content, 'html.parser')

list_data = soup.find_all('tr')

for data in list_data:
    print(data.get_text().encode('utf-8'), '\n')
#artist_name_list = soup.find(class_='BodyText')
#artist_name_list_items = artist_name_list.find_all('a')
#
#for artist_name in artist_name_list_items:
#    print(artist_name.prettify())

