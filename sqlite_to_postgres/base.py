import os

# по сколько строк встравлять в таблицу
WRITE_NUMBER_OF_ROWS = 100
# делитель по сколько читать
N_TIMES = 4

# коннект к бд
DATABASE = {
    'dbname': 'movies',
    'user': 'postgres',
    'password': 'password',
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=content'
}

SQLITE_FN = '../sqlite_to_postgres/db.sqlite'
SCHEMA_DESIGN_FN = '../schema_design/db_schema.sql'
