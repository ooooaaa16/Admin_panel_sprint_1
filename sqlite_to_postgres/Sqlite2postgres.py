import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import uuid
from dataclasses import dataclass, field

import datetime
from datetime import datetime

import logging

from base import *

@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Film_Work:
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    rating: str
    type: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre_Film_Work:
    created_at: datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person_Film_Work:
    role: str
    created_at: datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


def create_db_schema_in_postgres(pg_conn: _connection, db_schema):
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute(open(db_schema).read())


def insert_into_table(pg_conn, args, table_name, column_names):
    # собирам в строку название колонок таблицы
    with pg_conn.cursor() as pg_cursor:
        v = columns = f""""""
        for c in column_names:
            columns = columns + f"""{c}, """
            v = v + f"""%s, """
        try:
            pg_cursor.executemany(f"""INSERT INTO {table_name} VALUES ({v[:-2]}) ON CONFLICT DO NOTHING""", args)
        except pg_cursor.DatabaseError as ex:
            logger.critical(ex)


def load_genre(connection: sqlite3.Connection, pg_conn: _connection):
    logger.info("It is loading table_name Genre")
    table_name = 'genre'
    column_names = ('id', 'name', 'description', 'creation_at', 'updated_at')

    # готовим переменные
    inserted_rows = 0

    # вычитываем по WRITE_NUMBER_OF_ROWS строк в sq.lite и встраляем в postgres
    cursor = connection.execute("select * from " + table_name)
    while rows := cursor.fetchmany(WRITE_NUMBER_OF_ROWS):
        genres = []
        for row in rows:
            genres.append(Genre(name=row[1], description=row[2], created_at=row[3], updated_at=row[4], id=row[0]))

        args = []
        for genre in genres:
            args.append([genre.id, genre.name, genre.description, genre.created_at, genre.updated_at])

        insert_into_table(pg_conn, args, table_name, column_names)

        inserted_rows = inserted_rows + len(genres)
    cursor.close()
    logger.info("It was inserted %  rows", inserted_rows)


def load_film_work(connection: sqlite3.Connection, pg_conn: _connection):
    logger.info("It is loading table_name Film_work")
    table_name = 'film_work'
    column_names = ('id', 'title', 'description', 'creation_date', 'certificate', 'file_path', 'rating', 'type',
                    'created_at', 'updated_at')

    # готовим переменные
    inserted_rows = 0

    # вычитываем по WRITE_NUMBER_OF_ROWS строк в sq.lite и встраляем в postgres
    cursor = connection.execute("select * from " + table_name)
    while rows := cursor.fetchmany(WRITE_NUMBER_OF_ROWS):
        film_works = []
        for row in rows:
            film_works.append(Film_Work(title=row[1], description=row[2], creation_date=row[3],
                                        certificate=row[4], file_path=row[5], rating=row[6], type=row[7],
                                        created_at=row[8],
                                        updated_at=row[9], id=row[0]))
        args = []
        for film_work in film_works:
            args.append([film_work.id, film_work.title, film_work.description, film_work.creation_date, film_work.certificate,
                         film_work.file_path, film_work.rating, film_work.type, film_work.created_at, film_work.updated_at])

        insert_into_table(pg_conn, args, table_name, column_names)

        inserted_rows = inserted_rows + len(film_works)
    cursor.close()
    logger.info("It was inserted %  rows", inserted_rows)


def load_person(connection: sqlite3.Connection, pg_conn: _connection):
    logger.info("It is loading table_name Person")
    table_name = 'person'
    column_names = ('id', 'full_name', 'birth_date', 'created_at', 'updated_at')

    # готовим переменные
    inserted_rows = 0

    # вычитываем по WRITE_NUMBER_OF_ROWS строк в sq.lite и встраляем в postgres
    cursor = connection.execute("select * from " + table_name)
    while rows := cursor.fetchmany(WRITE_NUMBER_OF_ROWS):
        persons = []
        for row in rows:
            persons.append(Person(full_name=row[1], birth_date=row[2], created_at=row[3], updated_at=row[4], id=row[0]))

        args = []
        for person in persons:
            args.append([person.id, person.full_name, person.birth_date, person.created_at, person.updated_at])

        insert_into_table(pg_conn, args, table_name, column_names)

        inserted_rows = inserted_rows + len(persons)
    cursor.close()
    logger.info("It was inserted % rows", inserted_rows)


def load_genre_film_work(connection: sqlite3.Connection, pg_conn: _connection):
    logger.info("It is loading table_name Genre_Film_Work")
    table_name = 'genre_film_work'
    column_names = ('id', 'film_work_id', 'genre_id', 'created_at')

    # готовим переменные
    inserted_rows = 0

    # вычитываем по WRITE_NUMBER_OF_ROWS строк в sq.lite и встраляем в postgres
    cursor = connection.execute("select * from " + table_name)
    while rows := cursor.fetchmany(WRITE_NUMBER_OF_ROWS):
        genre_film_works = []
        for row in rows:
            genre_film_works.append(Genre_Film_Work(film_work_id=row[1], genre_id=row[2], created_at=row[3],
                                                    id=row[0]))
        args = []
        for genre_film_work in genre_film_works:
            args.append([genre_film_work.id, genre_film_work.film_work_id, genre_film_work.genre_id,
                         genre_film_work.created_at])

        insert_into_table(pg_conn, args, table_name, column_names)

        inserted_rows = inserted_rows + len(genre_film_works)
    cursor.close()
    logger.info("It was inserted % rows", inserted_rows)


def load_person_film_work(connection: sqlite3.Connection, pg_conn: _connection):
    logger.info("It is loading table_name Person_Film_Work")
    table_name = 'person_film_work'
    column_names = ('id', 'film_work_id', 'person_id', 'role', 'created_at')

    # готовим переменные
    inserted_rows = 0

    # вычитываем по WRITE_NUMBER_OF_ROWS строк в sq.lite и встраляем в postgres
    cursor = connection.execute("select * from " + table_name)
    while rows := cursor.fetchmany(WRITE_NUMBER_OF_ROWS):
        person_film_works = []
        for row in rows:
            person_film_works.append(Person_Film_Work(film_work_id=row[1], person_id=row[2], role=row[3],
                                                      created_at=row[4], id=row[0]))
        args = []
        for person_film_work in person_film_works:
            args.append([person_film_work.id, person_film_work.film_work_id, person_film_work.person_id,
                         person_film_work.role, person_film_work.created_at])

        insert_into_table(pg_conn, args, table_name, column_names)

        inserted_rows = inserted_rows + len(person_film_works)
    cursor.close()
    logger.info("It was inserted % rows", inserted_rows)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    """ В функцих заложено преобразование с соответствующих таблиц"""
    logger.info("It is starting of loading")
    load_genre(connection, pg_conn)
    load_film_work(connection, pg_conn)
    load_person(connection, pg_conn)
    load_genre_film_work(connection, pg_conn)
    load_person_film_work(connection, pg_conn)
    logger.info("That's all")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.info("Привет")

    try:
        with psycopg2.connect(**DATABASE, cursor_factory=DictCursor) as pg_conn:
            create_db_schema_in_postgres(pg_conn, SCHEMA_DESIGN_FN)
            pg_conn.commit()

        sqlite_conn=sqlite3.connect(SQLITE_FN)
        pg_conn=psycopg2.connect(**DATABASE,cursor_factory=DictCursor)
        load_from_sqlite(sqlite_conn, pg_conn)

        sqlite_conn.commit()
        pg_conn.commit()

    except (psycopg2.DatabaseError, sqlite3.Error, NameError, Exception) as ex:
        logger.critical(ex)
    finally:
        sqlite_conn.close()
        pg_conn.close()
