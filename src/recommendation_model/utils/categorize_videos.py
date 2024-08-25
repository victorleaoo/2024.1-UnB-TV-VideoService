from typing import List

from utils.model import IVideo, Catalog

# Função para categorizar vídeos
def categorize_videos(videos: List[IVideo], catalog: Catalog) -> None:
    keywords_categories = [
        {
            "keywords": ['fala, jovem'],
            "category": catalog.journalism["falaJovem"],
            "categoria": "Jornalismo",
        },
        {
            "keywords": ['informe unb'],
            "category": catalog.journalism["informeUnB"],
            "categoria": "Jornalismo",
        },
        {
            "keywords": ['zapping'],
            "category": catalog.journalism["zapping"],
            "categoria": "Jornalismo",
        },
        {
            "keywords": ['brasil em questão'],
            "category": catalog.interviews["brasilEmQuestao"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['diálogos'],
            "category": catalog.interviews["dialogos"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['tirando de letra'],
            "category": catalog.interviews["tirandoDeLetra"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['entrevista'],
            "category": catalog.interviews["entrevistas"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['vasto mundo'],
            "category": catalog.interviews["vastoMundo"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['vozes diplomáticas'],
            "category": catalog.interviews["vozesDiplomaticas"],
            "categoria": "Entrevista",
        },
        {
            "keywords": ['explique sua tese'],
            "category": catalog.researchAndScience["expliqueSuaTese"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['fazendo ciência'],
            "category": catalog.researchAndScience["fazendoCiencia"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['radar da extensão'],
            "category": catalog.researchAndScience["radarDaExtencao"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['se liga no pas'],
            "category": catalog.researchAndScience["seLigaNoPAS"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['unbtv ciência'],
            "category": catalog.researchAndScience["unbTvCiencia"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['universidade pra quê?', 'universidade para quê?'],
            "category": catalog.researchAndScience["universidadeParaQue"],
            "categoria": "Pesquisa e Ciência",
        },
        {
            "keywords": ['[em]cantos'],
            "category": catalog.artAndCulture["emCantos"],
            "categoria": "Arte e Cultura",
        },
        {
            "keywords": ['casa do som'],
            "category": catalog.artAndCulture["casaDoSom"],
            "categoria": "Arte e Cultura",
        },
        {
            "keywords": ['esboços'],
            "category": catalog.artAndCulture["esbocos"],
            "categoria": "Arte e Cultura",
        },
        {
            "keywords": ['exclusiva'],
            "category": catalog.artAndCulture["exclusiva"],
            "categoria": "Arte e Cultura",
        },
        {
            "keywords": ['floresta de gente'],
            "category": catalog.specialSeries["florestaDeGente"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": ['guia do calouro'],
            "category": catalog.specialSeries["guiaDoCalouro"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": ['memórias sobre paulo freire'],
            "category": catalog.specialSeries["memoriasPauloFreire"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": ['desafios das eleições'],
            "category": catalog.specialSeries["desafiosDasEleicoes"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": ['vida de estudante'],
            "category": catalog.specialSeries["vidaDeEstudante"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": ['arquitetura'],
            "category": catalog.specialSeries["arquiteturaICC"],
            "categoria": "Séries Especiais",
        },
        {
            "keywords": [
                'mini doc',
                'cerrado de volta',
                'construção tradicional kalunga',
                'o muro',
                'um lugar para onde voltar',
                'vidas no cárcere',
            ],
            "category": catalog.documentaries["miniDoc"],
            "categoria": "Documentais",
        },
        {
            "keywords": [
                'documentários',
                'documentário',
                'quanto vale um terço?',
                'refazendo os caminhos de george gardner',
                'sem hora para chegar',
                'todas podem ser vítimas',
            ],
            "category": catalog.documentaries["documentaries"],
            "categoria": "Documentais",
        },
        {
            "keywords": ['pitadas do cerrado'],
            "category": catalog.varieties["pitadasDoCerrado"],
            "categoria": "Variedades",
        },
    ]

    for video in videos:
        keywords_title = video.title.lower()
        category = next((config for config in keywords_categories if any(keyword in keywords_title for keyword in config["keywords"])), None)
        if category:
            video.catalog = category["categoria"]
            category["category"].append(video)
        else:
            video.catalog = "UnBTV"
            catalog.unbtv.append(video)