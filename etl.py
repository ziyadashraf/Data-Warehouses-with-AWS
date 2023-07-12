import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Loaded")
    except psycopg2.Error as e:
        print(e)


def insert_tables(cur, conn):
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()

        print("Tables Inserted")

    except psycopg2.Error as e:
        print(e)


def main():
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
