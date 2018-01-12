import requests
from bs4 import BeautifulSoup
from urllib import request, parse
#quote_page = input("Ingresa la pagina web:")

page = requests.post('https://enlinea.sunedu.gob.pe/programa')

soup = BeautifulSoup(page.content, 'html.parser')

list_data = soup.find_all('tr')
datos={}
count = 0
for data in list_data:
	count++	
	td_list = data.find_all('td')
	#datos[codigo] = td_list[0].get_text().encode('utf-8')
	datos[institucion_nombre[count]] = ("df")
	#datos[grado] = ("df")
	#datos[carrera] = ("df")

print(datos)
#artist_name_list = soup.find(class_='BodyText')
#artist_name_list_items = artist_name_list.find_all('a')
#
#for artist_name in artist_name_list_items:
#    print(artist_name.prettify())

