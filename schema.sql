-- Estrutura do banco de dados do MovieFinder
-- Criado a partir das informações verificadas no PostgreSQL.
-- Execute em um banco vazio destinado ao projeto.
-- Este script não apaga tabelas nem dados existentes.

CREATE TABLE public.tblfilmes (
    id integer GENERATED ALWAYS AS IDENTITY,
    tmdb_id integer NOT NULL,
    titulo character varying(100) NOT NULL,
    ano integer NOT NULL,
    nota numeric(5,3) NOT NULL,
    sinopse text,
    duracao integer,
    favorito boolean NOT NULL DEFAULT false,
    CONSTRAINT tblfilmes_pkey PRIMARY KEY (id),
    CONSTRAINT tblfilmes_tmdb_id_key UNIQUE (tmdb_id)
);

CREATE TABLE public.tblgeneros (
    id serial NOT NULL,
    tmdb_id integer NOT NULL,
    nome character varying(100) NOT NULL,
    CONSTRAINT tblgeneros_pkey PRIMARY KEY (id),
    CONSTRAINT tblgeneros_tmdb_id_key UNIQUE (tmdb_id)
);

CREATE TABLE public.tblfilmegeneros (
    filme_id integer NOT NULL,
    genero_id integer NOT NULL,
    CONSTRAINT tblfilmegeneros_pkey PRIMARY KEY (filme_id, genero_id),
    CONSTRAINT tblfilmegeneros_filme_id_fkey
        FOREIGN KEY (filme_id) REFERENCES public.tblfilmes (id),
    CONSTRAINT tblfilmegeneros_genero_id_fkey
        FOREIGN KEY (genero_id) REFERENCES public.tblgeneros (id)
);

CREATE TABLE public.tbldisponibilidade (
    id serial NOT NULL,
    tmdb_id integer NOT NULL,
    provider_id integer NOT NULL,
    provider_name character varying(100) NOT NULL,
    tipo character varying(20) NOT NULL,
    logo_path character varying(100),
    link character varying(255),
    CONSTRAINT tbldisponibilidade_pkey PRIMARY KEY (id)
);

