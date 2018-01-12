import urllib2
from bs4 import BeautifulSoup
quote_page = input("Ingresa la pagina web:")

#Obtengo la pagina que retorna su html
page = urllib2.urlopen(quote_page)

#Parseo el html usando la libraria beautiful
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('table')

print(name_box)

