import psycopg2
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ESSE Pipeline pega um registro, verifica se ele identificou uma ou mais cidades e doenças e insere na base de dados
class PostgresqlPipeline(object):

    def open_spider(self, spider):

        self.con = psycopg2.connect(
            host=os.environ.get("DATABASE_HOST"), 
            database=os.environ.get("DATABASE_DB"), 
            user=os.environ.get("DATABASE_USER"), 
            password=os.environ.get("DATABASE_PASSWORD"))
        self.cur = self.con.cursor()

        # Limpa os dados da cidade antes de executar o spider novamente
        # self.cur.execute(
        #     "DELETE FROM crawling.public_health WHERE cidade = %s", (spider.name,))
        # self.con.commit()

        #logging.warning('Spider aberto')

    def close_spider(self, spider):
        self.cur.close()
        self.con.close()
        #logging.warning('Spider Fechou')

    # Salvando cada item na base de dados
    def process_item(self, item, spider):
        if(len(item['doencas']) > 0 and (not (not item['cidades']))):
            try:
                self.cur.execute("INSERT INTO crawling.crawling_news(cidades, titulo, doencas, data, url, tipo) VALUES (%s,%s,%s,%s,%s,%s)",
                                 (json.dumps(item['cidades']), item['titulo'], item['doencas'], item['data'], item['url'], item['tipo']))
                self.con.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                self.con.rollback()

        return item