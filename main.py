import psycopg2
import os

def create_db(connect) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client (
            id serial PRIMARY KEY,
            name VARCHAR(20) not null,
            last_name VARCHAR(20) not null,
            email VARCHAR(40) not null,
            phone VARCHAR(20)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_number (
            id serial PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            number VARCHAR(20) not null,
            UNIQUE (number)
            );
        """)
        connect.commit()

def add_client(connect, client_name: str, client_last_name: str, client_email: str, number=None) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            INSERT INTO client (name, last_name, email, phone) VALUES (%s, %s, %s, %s);
        """, (client_name, client_last_name, client_email, number,))
        connect.commit()

def add_phone(connect, add_client_id: int, number_phone: str) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            INSERT INTO phone_number(client_id, number) VALUES (%s, %s);
        """, (add_client_id, number_phone))
        connect.commit()

def drop_client(connect) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DROP TABLE client;
        """)
        connect.commit()

def drop_phone(connect) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DROP TABLE phone_number;
        """)
        connect.commit()

def update_clientInfo(connect, client_id: int, client_name: str = None, client_last_name: str = None, client_email: str = None, client_phone: str = None) -> None:
    with connect.cursor() as cur:
        if client_name != None:
            cur.execute("""
                UPDATE client SET name=%s WHERE id=%s;
            """, (client_name, client_id,))
        elif client_last_name != None:
            cur.execute("""
                UPDATE client SET last_name=%s id=%s;
            """, (client_last_name, client_id,))
        elif client_email != None:
            cur.execute("""
                UPDATE client SET email=%s id=%s;
            """, (client_email, client_id,))
        elif client_phone != None:
            cur.execute("""
                UPDATE client SET phone=%s id=%s;
            """, (client_phone, client_id,))

def delete_clientPhone(connect, client_id: int, client_phone: str) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DELETE FROM phone_number WHERE client_id=%s AND number=%s;
        """, (client_id, client_phone,))

def delete_client(connect, client_id: int) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DELETE FROM phone_number WHERE id=%s;
        """, (client_id,))

def find_client(connect, client_name: str=None, client_last_name: str=None, client_email: str=None, client_phone: str=None) -> None:
    with connect.cursor() as cur:
        if client_name != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone, b.number AS additional_number FROM client a, phone_number b
                WHERE a.id=b.client_id AND a.name=%s
                GROUP BY a.id, b.number;
            """, (client_name,))
            print(cur.fetchall())
        elif client_last_name != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone, b.number as additional_number FROM client a, phone_number b
                WHERE a.id=b.client_id AND a.last_name=%s
                GROUP BY a.id, b.number;
            """, (client_last_name,))
            print(cur.fetchall())
        elif client_email != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone, b.number as additional_number FROM client a, phone_number b
                WHERE a.id=b.client_id AND a.email=%s
                GROUP BY a.id, b.number;
            """, (client_email,))
            print(cur.fetchall())
        elif client_phone != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone, b.number as additional_number FROM client a, phone_number b
                WHERE a.id=b.client_id AND (a.phone=%s OR b.number=%s)
                GROUP BY a.id, b.number;
            """, (client_phone, client_phone))
            print(cur.fetchall())

with psycopg2.connect(database="netology_db", user="postgres", port='5431') as conn:
    create_db(conn)
    add_client(conn, 'Gleb', 'Litvinenko', 'gleb@gmail.com', '+21')
    find_client(conn, client_phone='+21')
