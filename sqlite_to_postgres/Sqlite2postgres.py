import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import uuid
from dataclasses import dataclass, field
import datetime
from datetime import datetime

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


def redefine_read_number(readed_number_of_rows):
    read_number_of_rows = WRITE_NUMBER_OF_ROWS // N_TIMES
    if read_number_of_rows + readed_number_of_rows > WRITE_NUMBER_OF_ROWS:
        read_number_of_rows = WRITE_NUMBER_OF_ROWS - readed_number_of_rows
    return read_number_of_rows


def insert_into_table(pg_cursor, args, table_name, column_names):
    # собирам в строку название колонок таблицы
    columns = f""""""
    for c in column_names:
        columns = columns + f"""{c}, """

    pg_cursor.execute(f"""INSERT INTO {table_name} ({columns[:-2]}) VALUES {args} ON CONFLICT DO NOTHING""")


def Load_Genre(connection: sqlite3.Connection, pg_conn: _connection):
    print("It is loading table_name Genre")
    table_name = 'genre'
    column_names = ('id', 'name', 'description', 'created_at', 'updated_at')
    cursor = connection.execute("select * from " + table_name)
    # читам по N строк
    rows = cursor.fetchmany(redefine_read_number(0))
    # готовим переменные
    inserted_rows = 0
    genres = []
    readed_number_of_rows = 0
    while rows:
        readed_number_of_rows = readed_number_of_rows + len(rows)
        # записываем строки в список dataclass

        for row in rows:
            genres.append(Genre(name=row[1], description=row[2], created_at=row[3], updated_at=row[4], id=row[0]))

        if readed_number_of_rows < WRITE_NUMBER_OF_ROWS:
            with pg_conn.cursor() as pg_cursor:
                args = ','.join(pg_cursor.mogrify(
                    "(%s, %s, %s, %s, %s)", [item.id, item.name, item.description, item.created_at, item.updated_at]
                ).decode() for item in genres)
                # вставляем в таблицу
                insert_into_table(pg_cursor, args, table_name, column_names)
            inserted_rows = inserted_rows + len(genres)
            # обнуляем переменные
            genres = []
            readed_number_of_rows = 0

        rows = cursor.fetchmany(redefine_read_number(0))
    cursor.close()
    print("It was processed % rows", inserted_rows)


def Load_Film_Work(connection: sqlite3.Connection, pg_conn: _connection):
    print("It is loading table_name Film_work")
    table_name = 'film_work'
    column_names = ('id', 'title', 'description', 'creation_date', 'certificate', 'file_path', 'rating', 'type',
                    'created_at', 'updated_at')

    cursor = connection.execute("select * from " + table_name)

    # читам по N строк
    rows = cursor.fetchmany(redefine_read_number(0))
    # готовим переменные
    inserted_rows = 0
    film_works = []
    readed_number_of_rows = 0
    while rows:
        readed_number_of_rows = readed_number_of_rows + len(rows)
        for row in rows:
            film_works.append(Film_Work(title=row[1], description=row[2], creation_date=row[3],
                                        certificate=row[4], file_path=row[5], rating=row[6], type=row[7],
                                        created_at=row[8],
                                        updated_at=row[9], id=row[0]))
        if readed_number_of_rows < WRITE_NUMBER_OF_ROWS:
            with pg_conn.cursor() as pg_cursor:
                args = ','.join(pg_cursor.mogrify(
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [item.id, item.title, item.description, item.creation_date,
                     item.certificate, item.file_path, item.rating, item.type, item.created_at,
                     item.updated_at]
                ).decode() for item in film_works)
                insert_into_table(pg_cursor, args, table_name, column_names)
            inserted_rows = inserted_rows + len(film_works)
            # обнуляем переменные
            film_works = []
            readed_number_of_rows = 0

        rows = cursor.fetchmany(redefine_read_number(0))
    cursor.close()

    print("It was inserted % rows", inserted_rows)


def Load_Person(connection: sqlite3.Connection, pg_conn: _connection):
    print("It is loading table_name Person")
    table_name = 'person'
    column_names = ('id', 'full_name', 'birth_date', 'created_at', 'updated_at')

    cursor = connection.execute("select * from " + table_name)

    # читам по N строк
    rows = cursor.fetchmany(redefine_read_number(0))
    # готовим переменные
    inserted_rows = 0
    persons = []
    readed_number_of_rows = 0
    while rows:
        readed_number_of_rows = readed_number_of_rows + len(rows)
        for row in rows:
            persons.append(Person(full_name=row[1], birth_date=row[2], created_at=row[3], updated_at=row[4],
                                  id=row[0]))
        if readed_number_of_rows < WRITE_NUMBER_OF_ROWS:
            with pg_conn.cursor() as pg_cursor:
                args = ','.join(pg_cursor.mogrify(
                    "(%s, %s, %s, %s, %s)", [item.id, item.full_name, item.birth_date, item.created_at,
                                             item.updated_at]
                ).decode() for item in persons)
                insert_into_table(pg_cursor, args, table_name, column_names)
            inserted_rows = inserted_rows + len(persons)
            # обнуляем переменные
            persons = []
            readed_number_of_rows = 0

        rows = cursor.fetchmany(redefine_read_number(0))
    cursor.close()

    print("It was inserted % rows", inserted_rows)


def Load_Genre_Film_Work(connection: sqlite3.Connection, pg_conn: _connection):
    print("It is loading table_name Genre_Film_Work")
    table_name = 'genre_film_work'
    column_names = ('id', 'film_work_id', 'genre_id', 'created_at')

    cursor = connection.execute("select * from " + table_name)

    # читам по N строк
    rows = cursor.fetchmany(redefine_read_number(0))
    # готовим переменные
    inserted_rows = 0
    genre_film_works = []
    readed_number_of_rows = 0
    while rows:
        readed_number_of_rows = readed_number_of_rows + len(rows)
        for row in rows:
            genre_film_works.append(Genre_Film_Work(film_work_id=row[1], genre_id=row[2], created_at=row[3],
                                                    id=row[0]))
        if readed_number_of_rows < WRITE_NUMBER_OF_ROWS:
            with pg_conn.cursor() as pg_cursor:
                args = ','.join(pg_cursor.mogrify(
                    "(%s, %s, %s, %s)", [item.id, item.film_work_id, item.genre_id, item.created_at]
                ).decode() for item in genre_film_works)
                insert_into_table(pg_cursor, args, table_name, column_names)
            inserted_rows = inserted_rows + len(genre_film_works)
            # обнуляем переменные
            genre_film_works = []
            readed_number_of_rows = 0

        rows = cursor.fetchmany(redefine_read_number(0))
    cursor.close()
    print("It was processed % rows", inserted_rows)


def Load_Person_Film_Work(connection: sqlite3.Connection, pg_conn: _connection):
    print("It is loading table_name Person_Film_Work")
    table_name = 'person_film_work'
    column_names = ('id', 'film_work_id', 'person_id', 'role', 'created_at')

    cursor = connection.execute("select * from " + table_name)

    # читам по N строк
    rows = cursor.fetchmany(redefine_read_number(0))
    # готовим переменные
    inserted_rows = 0
    person_film_works = []
    readed_number_of_rows = 0
    while rows:
        readed_number_of_rows = readed_number_of_rows + len(rows)
        for row in rows:
            person_film_works.append(Person_Film_Work(film_work_id=row[1], person_id=row[2], role=row[3],
                                                      created_at=row[4], id=row[0]))
        if readed_number_of_rows < WRITE_NUMBER_OF_ROWS:
            with pg_conn.cursor() as pg_cursor:
                args = ','.join(pg_cursor.mogrify(
                    "(%s, %s, %s, %s, %s)", [item.id, item.film_work_id, item.person_id, item.role, item.created_at]
                ).decode() for item in person_film_works)
                insert_into_table(pg_cursor, args, table_name, column_names)
            inserted_rows = inserted_rows + len(person_film_works)
            # обнуляем переменные
            person_film_works = []
            readed_number_of_rows = 0

        rows = cursor.fetchmany(redefine_read_number(0))
    cursor.close()
    print("It was processed % rows", inserted_rows)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    print("It is starting of loading")
    Load_Genre(connection, pg_conn)
    Load_Film_Work(connection, pg_conn)
    Load_Person(connection, pg_conn)
    Load_Genre_Film_Work(connection, pg_conn)
    Load_Person_Film_Work(connection, pg_conn)
    print("That's all")


# по сколько строк встравлять в таблицу
WRITE_NUMBER_OF_ROWS = 100
# делитель по сколько читать
N_TIMES = 4

if __name__ == '__main__':
    dsl = {
        'dbname': 'movies',
        'user': 'postgres',
        'password': 'password',
        'host': '127.0.0.1',
        'port': 5432,
        'options': '-c search_path=content'
    }
    if N_TIMES > WRITE_NUMBER_OF_ROWS: N_TIMES = 1
    try:
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            create_db_schema_in_postgres(pg_conn, 'db_schema.sql')
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except psycopg2.DatabaseError as ex:
        print(ex)
    except sqlite3.Error as ex:
        print(ex)
    except Exception as ex:
        print(ex)
