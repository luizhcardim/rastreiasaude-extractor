# Rastreia Saúde - Extrator

This project tracks diseases throught unstructured data (news),  GIS techniques, and machine learning.

## How to run:

First, create the database tables on PostgreSQL, using the script "tables_rastreia.sql".

Then, add a .env file at the project root with the following variables:

```bash
DATABASE_HOST=localhost
DATABASE_DB=<name of database>
DATABASE_USER=<user>
DATABASE_password=<password>
```

Then, add all the project requirements:

```bash
pip install -r requirements.txt
```

Then download the Portuguese model for Space:

```bash
python -m spacy download pt_core_news_sm
```

Then you can run the project crawlers:

```bash
scrapy crawl <name of crawling script>
```



