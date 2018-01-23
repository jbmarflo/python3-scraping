import pymysql.cursors
# pip install PyMySQL
class Query:
    def __init__(self, object, query, variables):
        self.connection = object
        self.query = query
        self.variables = variables
    
    def insert(object, text):
        return 4
    
    def select(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.query, self.variables)
            return cursor.fetchone()

class Server:
    def __init__(self):
        self.connection = pymysql.connect(host='qeestudiar.cpkdji7ctubu.us-west-2.rds.amazonaws.com',
                                          user='jbmarflo',
                                          password='pokemonqeestudiar*10',
                                          db='qeestudiar_db',
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
