CREATE TABLE dm_item_despesa (
    id_item_despesa              INTEGER NOT NULL,
    desc_item_despesa            VARCHAR(100)
);

ALTER TABLE dm_item_despesa ADD CONSTRAINT dm_item_despesa_pk PRIMARY KEY (id_item_despesa);

CREATE TABLE dm_credor (
    id_credor              SERIAL PRIMARY KEY,
    codigo_nacional_credor VARCHAR(18) NOT NULL,
    desc_credor            VARCHAR(100) NOT NULL,
    UNIQUE (codigo_nacional_credor, desc_credor)
);

CREATE TABLE dm_responsavel (
    id_unidade   INTEGER NOT NULL,
    id_orgao     INTEGER,
    desc_unidade VARCHAR(60),
    desc_orgao   VARCHAR(45)
);

ALTER TABLE dm_responsavel ADD CONSTRAINT dm_responsavel_pk PRIMARY KEY (id_unidade);

CREATE TABLE dm_temporal (
    id_data INTEGER NOT NULL,
    ano     INTEGER,
    mes     INTEGER,
    desc_mes VARCHAR,
    dia     INTEGER
);

ALTER TABLE dm_temporal ADD CONSTRAINT dm_temporal_pk PRIMARY KEY (id_data);

CREATE TABLE dm_tipo_despesa (
    id_tipo_despesa   INTEGER NOT NULL,
    desc_tipo_despesa VARCHAR(100)
);

ALTER TABLE dm_tipo_despesa ADD CONSTRAINT dm_tipo_despesa_pk PRIMARY KEY (id_tipo_despesa);

CREATE TABLE ft_despesas (
    id_unidade        INTEGER NOT NULL,
    id_tipo_despesa   INTEGER NOT NULL,
    id_credor         INTEGER NOT NULL,
    id_data           INTEGER NOT NULL,
    id_item_despesa   INTEGER NOT NULL,
    id_despesa        INTEGER NOT NULL,
    desc_despesa      VARCHAR,
    valor_empenhado   VARCHAR,
    valor_reforcado   VARCHAR,
    valor_liquidado   VARCHAR,
    valor_pago        VARCHAR,
    valor_retido      VARCHAR,
    valor_anulado     VARCHAR,
    PRIMARY KEY (id_unidade, id_tipo_despesa, id_credor, id_data, id_item_despesa, id_despesa),
    FOREIGN KEY (id_credor) REFERENCES dm_credor (id_credor),
    FOREIGN KEY (id_unidade) REFERENCES dm_responsavel (id_unidade),
    FOREIGN KEY (id_data) REFERENCES dm_temporal (id_data),
    FOREIGN KEY (id_tipo_despesa) REFERENCES dm_tipo_despesa (id_tipo_despesa),
    FOREIGN KEY (id_item_despesa) REFERENCES dm_item_despesa (id_item_despesa)
);
