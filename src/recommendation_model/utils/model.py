from typing import List, Optional

class IVideo:
    def __init__(self, id: int, title: str, description: Optional[str] = ''):
        self.id = id
        self.title = title
        self.description = description
        self.catalog = None  # Será preenchido após a categorização

class Catalog:
    def __init__(self):
        self.journalism = {
            "falaJovem": [],
            "informeUnB": [],
            "zapping": []
        }
        self.interviews = {
            "brasilEmQuestao": [],
            "dialogos": [],
            "tirandoDeLetra": [],
            "entrevistas": [],
            "vastoMundo": [],
            "vozesDiplomaticas": []
        }
        self.researchAndScience = {
            "expliqueSuaTese": [],
            "fazendoCiencia": [],
            "radarDaExtencao": [],
            "seLigaNoPAS": [],
            "unbTvCiencia": [],
            "universidadeParaQue": []
        }
        self.artAndCulture = {
            "emCantos": [],
            "casaDoSom": [],
            "esbocos": [],
            "exclusiva": []
        }
        self.specialSeries = {
            "florestaDeGente": [],
            "guiaDoCalouro": [],
            "memoriasPauloFreire": [],
            "desafiosDasEleicoes": [],
            "vidaDeEstudante": [],
            "arquiteturaICC": []
        }
        self.documentaries = {
            "miniDoc": [],
            "documentaries": []
        }
        self.varieties = {
            "pitadasDoCerrado": []
        }
        self.unbtv = []