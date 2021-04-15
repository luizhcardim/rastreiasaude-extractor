class NewsCategoryPipeline(object):


    #reg_campanha = re.compile('Campanha|Fevereiro Roxo|Setembro Amarelo|Outubro Rosa|Novembro Azul|Dezembro Vermelho',re.IGNORECASE)


    def process_item(self, item, spider):
        #tipo = 'Campanha' if self.reg_campanha.search(item['conteudo'],re.IGNORECASE) else ''

        item['tipo'] = ''
        return item

