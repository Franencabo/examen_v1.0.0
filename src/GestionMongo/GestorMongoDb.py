from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from datetime import datetime
import bson.objectid

class GestorMongoDb:

    def __init__(self):
        self.MONGO_URL_ATLAS = 'mongodb+srv://Franencabo:Aerobictotal2019@cluster0-8p1xr.mongodb.net/test?retryWrites=true&w=majority'
        self.cliente: MongoClient = None
        self.db: Database = None


    def conectarDB(self, db, coleccion):
        try:
            self.cliente = MongoClient(
                self.MONGO_URL_ATLAS, ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.coleccion_coche = self.db[coleccion]
            self.coleccion_usuarios = self.db['usuarios']
    
           
        except:
            raise Exception("Fallo en la base de datos.")

    def nuevo_registro(self, nick, email, password):
        fecha = datetime.now()
        registrar = self.coleccion_usuarios.insert_one({
            "nick": nick,
            "email": email,
            "password": password,
            "fecha": fecha
        })

    def busqueda_por_email(self, email):
        busqueda_por_email = list(self.coleccion_usuarios.find({'email': email}))
        return busqueda_por_email

    def creargastos(self, titulo, texto):
        fecha = datetime.now()
        creargastos = self.coleccion_coche.insert_one({'fecha':fecha, 'titulo': titulo,  'texto':texto})
        return creargastos
    
    def vergastos_ordenados(self):
        vergastos = self.coleccion_coche.find({}).sort("fecha", 1)
        return vergastos
    




gestormongo = GestorMongoDb()
gestormongo.conectarDB(db="gastos", coleccion="coche")
