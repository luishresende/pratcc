import os
import sqlite3

# Caminho do banco SQLite que será criado
database_path = "../database.db"

# Arquivos SQL a serem executados
sql_files = [
    "script_sqlite.sql",
    "states.sql",
    "cities.sql",
    "utfpr.sql"
]

if os.path.exists(database_path):
    os.remove(database_path)

def execute_sql_file(cursor, filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        sql_script = file.read()
        cursor.executescript(sql_script)
        print(f"Executado: {filepath}")

def main():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for sql_file in sql_files:
        execute_sql_file(cursor, sql_file)

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso.")

if __name__ == "__main__":
    main()
