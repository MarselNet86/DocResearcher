import psycopg2


class Database:
    def __init__(self, host, user, password, database, port):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.connection.autocommit = True

    def get_version(self):
        """Получить версию СУБД PostgreSQL"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f'Server version: {cursor.fetchone()[0]}')
