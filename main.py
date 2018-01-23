import requests
import uuid
import pymysql.cursors
from bs4 import BeautifulSoup
from urllib import request, parse
# pip install PyMySQL
class Query:
    def __init__(self, object, query, variables):
        self.connection = object
        self.query = query
        self.variables = variables
    
    def insert(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.query, self.variables)
        self.connection.commit()
    def select(self):
        with self.connection.cursor() as cursor:
                cursor.execute(self.query, self.variables)
                return cursor.fetchone()
class Server:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456*10',
                                         db='test',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

    def query(self, query, variables):
        try:
            return Query(self.connection, query, variables)
        except IndexError:
            return null

    def close(self):
        try:
            self.connection.close()
        except IndexError:
            print('No se puedo cerrar coneccion')
class Util:
    @staticmethod
    def slug(text):
        string = (text.lower()
                  .replace(' ', '-').replace(',', '-').replace('á', 'a')
                  .replace('é', 'e').replace('í', 'i').replace('ó', 'o')
                  .replace('ú', 'u').replace('ñ', 'n').replace('/', '-')
                  .replace('¨', '').replace('º', '').replace('~', '')
                  .replace('!', '').replace('(', '').replace(')', '')
                  .replace('?', '').replace('¿', '').replace(';', '-')
                  .replace('+', '-').replace('=', '-').replace('_', '-')
                  .replace('"', '').replace('|', '-').replace('\\', '-')
                  .replace('ü', 'u').replace('õ', 'o')
                  ) #áéíóú ñ
        return string
    @staticmethod
    def changeGrade(text):
        return {
                    'BACHILLER': 'bachelor',
                    'MAESTRO':'master',
                    'DOCTOR': 'doctorate'
                }[text]
#def scrapingGoogle(search):
#    page = requests.post('https://google.com/search?q=universidad-' + search)
#    soup = BeautifulSoup(page.content, 'html.parser')
#    image = soup.find('.kno-fb-ctx')
#    print(image)

def scraping(pageContent):
    soup = BeautifulSoup(pageContent, 'html.parser')
    list_data = soup.find_all('tr')
    datos={}
    list_data.pop(0) #Elimino los titulos de la tabla
    for i,row in enumerate(list_data):
        td_list = row.find_all('td')
        try:
            datos[int(td_list[0].get_text())] = {
                'codigo': int(td_list[0].get_text()),
                'institucionId': str(uuid.uuid4()),
                'institucion': td_list[1].get_text(),
                'institucionSlug': Util.slug(td_list[1].get_text()),
                'grado': Util.changeGrade(td_list[2].get_text()),
                'carreraId': str(uuid.uuid4()),
                'carrera': td_list[3].get_text(),
                'carreraSlug': Util.slug(td_list[3].get_text())
        }
        except IndexError:
            print('error en el primer index: ', i)
    return datos

def requestPage():
    maxValPage = 599 #Tienen 599 paginas
    data = {}
    page = 574
    server = Server()
    while page <= maxValPage:
        params = {'valPage': page}
        webPage = requests.post('https://enlinea.sunedu.gob.pe/programa', params=params)
        data = scraping(webPage.content)
        for row in data:
            try:
                # Treae la carrera si en caso existe
                carreraID = server.query(
                                                str("SELECT `id` FROM `career` WHERE `slug` = %s"),
                                                (data[row]['carreraSlug'])
                                                ).select()
                # consultar la bd si no existe institucion con el mismo slug
                institucionID = server.query(
                                         str("SELECT `id` FROM `institution` WHERE `username` = %s"),
                                         (data[row]['institucionSlug'])
                                         ).select()
                                         
                institutionHaveCareer = server.query(
                                                     str("SELECT `ci`.`institution_id` FROM `career_institution` `ci` " +
                                                         "INNER JOIN `institution` `i` ON `ci`.`institution_id` = `i`.`id`" +
                                                         "INNER JOIN `career` `c` ON `ci`.`career_id` = `c`.`id`" +
                                                         "WHERE `i`.`username` = %s" +
                                                         "AND  `c`.`slug` =  %s" +
                                                         "AND `ci`.`grade` = %s"),
                                                     (data[row]['institucionSlug'], data[row]['carreraSlug'], data[row]['grado'])
                                         ).select()
#                scrapingGoogle(data[row]['institucionSlug'])
                # Validar si la institucion cuenta ese proyecto
                if carreraID is None:
                    #Insertar carrera
                    server.query(
                        str("INSERT INTO `career`(`id`, `name`, `slug`) VALUES (%s, %s, %s)"),
                        (data[row]['carreraId'], data[row]['carrera'], data[row]['carreraSlug'])
                    ).insert()
                    print('Carrera Slug: -> subio ', data[row]['codigo'], '\n')
#                    print(data[row]['carreraId'], '\n')
                if institucionID is None:
                    # Insertar institucion
                    server.query(
                         str("INSERT INTO `institution`(`id`, `username`, `name`) VALUES (%s, %s, %s)"),
                         (data[row]['institucionId'], data[row]['institucionSlug'], data[row]['institucion'])
                    ).insert()
                    print('Institucion slug: ',data[row]['institucionSlug'],' -> subio ', data[row]['codigo'], '\n')
#                    print(data[row]['institucionId'], '\n')
                if institutionHaveCareer is None:
                    #Insertar pertenecia con su grado
                    if carreraID is not None and institucionID is not None:
                            server.query(
                                 str("INSERT INTO `career_institution`(`institution_id`, `career_id`, `grade`) VALUES (%s, %s, %s)"),
                                 (institucionID['id'], carreraID['id'], data[row]['grado'])
                            ).insert()
#                    print(data[row]['institucionId'], '\n')
            except IndexError:
                print(data[row]['codigo'], ' -> error', '\n')
        page += 1
    server.close()
    return 0

requestPage()
