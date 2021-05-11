-- Schema Definition ---------------------------------------------
CREATE SCHEMA crawling;

-- Table Definition ----------------------------------------------

CREATE TABLE crawling.crawling_news (
    url character varying(500) PRIMARY KEY,
    cidades jsonb NOT NULL,
    titulo character varying(500) NOT NULL,
    doencas character varying(50)[],
    data date,
    tipo character varying(20),
    tipo_predicted character varying(20),
    is_case smallint
);

CREATE UNIQUE INDEX crawling_news_pkey1 ON crawling.crawling_news(url text_ops);

CREATE TABLE crawling.municipios (
    id integer DEFAULT nextval('crawling.municipios_id_seq'::regclass) PRIMARY KEY,
    geom geometry(MultiPolygon,4326),
    cd_mun character varying(7),
    nm_mun character varying(60),
    sigla_uf character varying(2),
    area_km2 double precision,
    populacao integer
);

CREATE UNIQUE INDEX municipios_pkey ON crawling.municipios(id int4_ops);
CREATE INDEX municipios_geom_idx ON crawling.municipios USING GIST (geom gist_geometry_ops_2d);

CREATE TABLE crawling.users (
    username character varying(40) PRIMARY KEY,
    password character varying(200) NOT NULL
);


CREATE UNIQUE INDEX users_pkey ON crawling.users(username text_ops);

-- Inserting a default user and password ---
INSERT INTO crawling.users(username, password) VALUES('admin','$2a$10$LQR9lAMzXQRAxSw7kRSHX.X1SPKK.WM/CogrSVDgCDzf1qHS/TYha')
