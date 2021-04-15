import pandas as pd
import numpy as np
import re
import spacy


class PlacesPipeline(object):

    def open_spider(self, spider):

        self.nlp = spacy.load('pt')
        self.municipios_br = pd.read_csv('publichealth/lib/places/municipios.csv')

    def close_spider(self, spider):
        print('Close Place Pipeline')
        #logging.warning('Spider Fechou')

    def chooseBestPlace(self, duplicated, places, source_UF):

        ret = places

        for dup in duplicated:
            homonimos = places[places.municipio == dup]

            mesmo_local_jornal = homonimos[homonimos['uf'] == source_UF]
            # Se alguma das cidades estiver no mesmo estado do jornal que publicou a notícia
            if (mesmo_local_jornal.size > 0):
                remover = homonimos[homonimos['uf'] != source_UF]
                ret = pd.concat([ret, remover]).drop_duplicates(keep=False)

            # Caso contrário seleciona a cidade com maior população
            else:
                remover = homonimos[~homonimos.index.isin([homonimos['populacao'].idxmax()])]
                ret = pd.concat([ret, remover]).drop_duplicates(keep=False)

        return ret

    # Filtra os municípios que são frequentemente identificados incorretamente
    # Nesse caso só aceita caso no texto também seja encontrada referência ao estado do município
    def filterPlaces(self,places):
        
        remove = pd.DataFrame({'remover':[
            'Paraná',
            'Esperança', # Município da Paraíba
            'Saúde', # Município da Bahia
            'Granja', # Município do Ceará
            'Prainha', # Município do Pará
            'Tailândia', # Pará
            'Colômbia', # São Paulo
            'União', #Piauí
            'Planalto', # Paraná
            'Natal' # RN

        ]})

        remover = places[places.municipio.isin(remove['remover'])]
        ret = pd.concat([places, remover]).drop_duplicates(keep=False)
        
        return ret 

    # Esse método verifica as cidades presentes no texto que estão no Brasil e já remove duplicados
    def findPlaces(self, text, municipios):

        places = self.filterPlaces(municipios[np.in1d(municipios['municipio'], text)])
        
        # Verificar se existem cidades com homônimos na lista
        duplicated = places[places.duplicated(['municipio'])]['municipio'].tolist()

        if len(duplicated) > 0:
            places = self.chooseBestPlace(duplicated, places, 'PR')
            # self.chooseBestPlace(duplicated, places, 'SP')

        # Testando quando municípios do brasil estão no texto
        # mun_br = municipios[np.in1d(municipios['municipio'], text)]
        return places

    


    # Salvando cada item na base de dados
    def process_item(self, item, spider):

        conteudo = ''.join(item['conteudo'])

        if (re.search("bairro|bairros", conteudo)):
            item['cidades'] = []
        else:
            doc = self.nlp(conteudo)
    

            places = [X.text if X.label_ == 'LOC' else None for X in doc.ents]
    
            item['cidades'] = self.findPlaces(places,self.municipios_br).to_dict('records')
    

        return item