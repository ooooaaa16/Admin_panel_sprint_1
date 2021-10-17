-- создание схемы в БД для контента
CREATE SCHEMA IF NOT EXISTS content;

 -- создаем таблицу жанры
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
	constraint pkey_tbl PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS content.film_work (
     id uuid NOT NULL DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
	constraint pkey_tbl PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work using BTREE(creation_date);

CREATE TABLE IF NOT EXISTS content.person (
   id uuid NOT NULL DEFAULT ugen_random_uuid(),
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
	constraint pkey_tbl PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
 	id uuid NOT NULL DEFAULT gen_random_uuid(),
    film_work_id uuid NOT NULL REFERENCES film_work (id),
    genre_id uuid NOT NULL REFERENCES genre (id),
    created_at timestamp with time zone,
	constraint pkey_tbl PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre ON content.genre_film_work  using BTREE(film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
  	id uuid NOT NULL DEFAULT gen_random_uuid (),
    film_work_id uuid NOT NULL REFERENCES film_work (id),
    person_id uuid NOT NULL REFERENCES person (id),
    role TEXT NOT NULL,
    created_at timestamp with time zone,
	constraint pkey_tbl PRIMARY KEY (id)
);            
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role ON content.person_film_work using BTREE(film_work_id, person_id, role);
