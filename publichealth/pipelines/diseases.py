import re

class DiseasesPipeline(object):
    # TODO:  Verificar como colocar PESTE e RAIVA
    doencas = [
        'covid',
        'corona-vírus',
        'coronavírus',
        'sarampo',
        'febre amarela',
        'dengue',
        'aedes',
        'hiv',
        'aids',
        'amebíase',
        'ancilostomíase',
        'ascaridíase',
        'botulismo',
        'brucelose',
        'cancro Mole',
        'candidíase',
        'coccidioidomicose',
        'cólera',
        'coqueluche',
        'criptococose',
        'criptosporidíase',
        'difteria',
        'doença de chagas',
        'doença de lyme',
        'doenças diarreicas agudas',
        'diarreia',
        'doença meningocócica',
        'donovanose',
        'enterobíase',
        'escabiose',
        'esquistossomose mansônica',
        'estrongiloidíase',
        'febre maculosa brasileira',
        'febre purpúrica brasileira',
        'febre tifóide',
        'filaríase',
        'giardíase',
        'gonorreia',
        'hanseníase',
        'hantaviroses',
        'hepatite a',
        'hepatite b',
        'hepatite c',
        'hepatite d',
        'hepatite e',
        'herpes',
        'histoplasmose',
        'hpv',
        'influenza',
        'leishmaniose',
        'leptospirose',
        'linfogranuloma',
        'malária',
        'meningite',
        'mononucleose',
        'oncocercose',
        'paracoccidioidomicose',
        'parotidite',
        'poliomielite',
        'psitacose',
        'rubéola',
        'shigelose',
        'sífilis',
        'teníase',
        'tênia',
        'cisticercose',
        'tétano',
        'toxoplasmose',
        'tracoma',
        'tuberculose',
        'varicela']

    sinonimos = [
        {
            'doenca': 'covid-19',
            'sinonimo': ['covid', 'coronavírus']
        },
        {
            'doenca': 'dengue',
            'sinonimo': ['aedes']
        },
        {
            'doenca': 'hiv',
            'sinonimo': ['aids']
        },
        {
            'doenca': 'influenza',
            'sinonimo':['gripe']
        }
    ]

    # Procura pelas doenças no conteúdo da notícia
    def process_item(self, item, spider):
        # item['doencas'] = "Testando se possui Aedes Febre Amarela".lower()
        encontradas = []
        t = ''.join(item['conteudo'])

        do = re.findall('|'.join(self.doencas), t.lower())
        for d in do:

            # Verificar sinônimo
            s = [x['doenca'] for x in self.sinonimos if x['sinonimo'].count(d)]

            if (len(s) > 0):
                d = s[0]

            if d not in encontradas:
                encontradas.append(d)

        item['doencas'] = encontradas

        return item
