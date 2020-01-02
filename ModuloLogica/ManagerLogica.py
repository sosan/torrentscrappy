from datetime import datetime
from datetime import timedelta
import ModuloWeb.managerWeb
import ModuloMongo.mongomanager
import random


class ManagerLogica:
    def __init__(self):
        self.managerweb = ModuloWeb.managerWeb.ManagerWeb()
        self.managermongo = ModuloMongo.mongomanager.managermongo

    def comprobaradmin(self, usuario, password):
        ok = self.managermongo.comprobaradmin(usuario, password)
        return ok

    def set_peliculas(self):
        resultados = self.managerweb.scrappyDonTorrent()

        if len(resultados) > 0:
            ok = self.managermongo.insertarurls(resultados)
        else:
            return False

    def getpeliculas(self):
        resultados = self.managermongo.getpeliculas()
        if len(resultados) > 0:
            return True, resultados
        else:
            return False, None

    def getseries(self):
        resultados = self.managermongo.getseries()
        if len(resultados) > 0:
            return True, resultados
        else:
            return False, None
