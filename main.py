import requests
import pymysql.cursors
from bs4 import BeautifulSoup
from urllib import request, parse
# pip install PyMySQL
class Server:
    def __init__(self):
        self.connection = pymysql.connect(host='qeestudiar.cpkdji7ctubu.us-west-2.rds.amazonaws.com',
                                         user='jbmarflo',
                                         password='pokemonqeestudiar*10',
                                         db='qeestudiar_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

    def insert(query):
            with self.connection.cursor() as cursor:
                # Create a new record
#                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                sql = query
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            self.connection.commit()
        
    def close():
        self.connection.close()

def scraping(pageContent):
    soup = BeautifulSoup(pageContent, 'html.parser')
    list_data = soup.find_all('tr')
    datos={}
    list_data.pop(0) #Elimino los titulos de la tabla
    for i,row in enumerate(list_data):
        td_list = row.find_all('td')
        try:
            datos[int(td_list[0].get_text().encode('utf-8'))] = {
                'codigo': int(td_list[0].get_text().encode('utf-8')),
                'institucion': td_list[1].get_text().encode('utf-8'),
                'grado': td_list[2].get_text().encode('utf-8'),
                'carrera': td_list[3].get_text().encode('utf-8')
        }
        except IndexError:
            print('error en el primer index: ', i)
    return datos



def requestPage():
    maxValPage = 2 #Tienen 599 paginas
    data = {}
    page = 1
    server = Server()
    while page <= maxValPage:
        params = {'valPage': page}
        webPage = requests.post('https://enlinea.sunedu.gob.pe/programa', params=params)
        data = scraping(webPage.content)
        for row in data:
            try:
#                server.insert('')
                print(data[row]['codigo'], ' -> subio', '\n')
            except IndexError:
                print(data[row]['codigo'], ' -> error', '\n')
        page += 1
    
    return 0

requestPage()
