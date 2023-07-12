import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Dropped")
    except psycopg2.Error as e:
        print(e)


def create_tables(cur, conn):
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables Created")

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

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()
    except psycopg2.Error as e:
        print(e)


if __name__ == "__main__":
    main()
