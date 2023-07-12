import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load data into staging tables.

    Parameters:
    cur (psycopg2.extensions.cursor): The database cursor.
    conn (psycopg2.extensions.connection): The database connection.

    Returns:
    None

    """
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Loaded")
    except psycopg2.Error as e:
        print(e)


def insert_tables(cur, conn):
    """
    Insert data from staging tables to dim and fact tables.

    Parameters:
    cur (psycopg2.extensions.cursor): The database cursor.
    conn (psycopg2.extensions.connection): The database connection.

    Returns:
    None
    """
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()

        print("Tables Inserted")

    except psycopg2.Error as e:
        print(e)


def main():
    """
    Calls functions to load data and insert them tables.

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

        load_staging_tables(cur, conn)
        insert_tables(cur, conn)

        conn.close()
    except psycopg2.Error as e:
        print(e)


if __name__ == "__main__":
    main()
