import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops the database tables.

    Parameters:
    cur (psycopg2.extensions.cursor): The database cursor.
    conn (psycopg2.extensions.connection): The database connection.

    Returns:
    None
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Dropped")
    except psycopg2.Error as e:
        print(e)


def create_tables(cur, conn):
    """
    Creates database tables.

    Parameters:
    cur (psycopg2.extensions.cursor): The database cursor.
    conn (psycopg2.extensions.connection): The database connection.

    Returns:
    None
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Created")

    except psycopg2.Error as e:
        print(e)


def main():
    """
    Calls functions to drop and create tables.

    Parameters:
    None

    Returns:
    None
    """
    try:
        config = configparser.ConfigParser()
        config.read("dwh.cfg")

        conn = psycopg2.connect(
            "host={} dbname={} user={} password={} port={}".format(
                *config["CLUSTER"].values()
            )
        )
        cur = conn.cursor()

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()
    except psycopg2.Error as e:
        print(e)


if __name__ == "__main__":
    main()
