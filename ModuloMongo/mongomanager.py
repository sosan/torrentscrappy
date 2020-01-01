import locale
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class ManagerMongoDb:
    def __init__(self):
        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db_webtorrent: Database = None
        self.cursorPeliculas: Collection = None
        self.cursorSeries: Collection = None
        self.cursorAdmin: Collection = None
        self.cursorAyuda: Collection = None

    def conectDB(self, usuario, password, host, db, coleccionPeliculas, coleccionSeries):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db_webtorrent = self.cliente[db]
            # serverStatusResult = self.db_webtorrent.command("serverStatus")
            self.cursorPeliculas = self.db_webtorrent[coleccionPeliculas]
            self.cursorSeries = self.db_webtorrent[coleccionSeries]
            self.cursorAdmin = self.db_webtorrent["admin"]
            self.cursorAyuda = self.db_webtorrent["ayuda"]

        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    def getLastFecha(self):
        resultados = list(self.cursorAyuda.find({"_id": "last_fecha_dontorrent"}))
        if len(resultados) > 0:
            fecha = resultados[0]["fecha"]
            return fecha
        return None

    def insertarurls(self, datos: dict):
        ok = self.cursorPeliculas.insert_one(datos)
        if ok.inserted_id != None:
            patron = {"_id": "last_fecha_dontorrent"}
            datosdb = self.cursorAyuda.find_one(patron)
            if "fecha" in datosdb:
                if datos["fecha"] > datosdb["fecha"]:
                    # actualizar
                    ok = self.cursorAyuda.update_one(patron, {"$set": {"fecha": datos["fecha"]}})
                    if ok.modified_count > 0:
                        print("Modificado fecha")
                    print(ok)
            return True
        return False

    def getpeliculas(self):
        ok = self.cursorPeliculas.find({})
        return ok

    def getseries(self):
        resultados = self.cursorPeliculas.find({})
        return resultados

    def encontrarTituloImagen(self, titulo, imagen):
        patron = {
            "imagen": imagen
        }

        ok = list(self.cursorPeliculas.find(patron))
        if len(ok) > 0:
            return True
        return False

    def comprobaradmin(self, usuario, password):
        ok = self.cursorAdmin.find_one({"usuario": usuario, "password": password}, {"_id": False})
        if ok is not None:
            return True
        return False


managermongo = ManagerMongoDb()
managermongo.conectDB("pepito", "pepito", "cluster0-9k9sv.azure.mongodb.net/test?retryWrites=true&w=majority",
                      db="webtorrent", coleccionPeliculas="peliculas", coleccionSeries="series")
