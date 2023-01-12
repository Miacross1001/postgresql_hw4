import psycopg2

def create_db(connect) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client (
            id serial PRIMARY KEY,
            name VARCHAR(20) not null,
            last_name VARCHAR(20) not null,
            email VARCHAR(40) CHECK (email LIKE '%@%'),
            phone VARCHAR(20) CHECK (phone LIKE '+%'),
            CONSTRAINT AD_client UNIQUE (id, email, phone)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_number (
            id serial PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            number VARCHAR(20) CHECK (number LIKE '+%'),
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
        if client_last_name != None:
            cur.execute("""
                UPDATE client SET last_name=%s WHERE id=%s;
            """, (client_last_name, client_id,))
        if client_email != None:
            cur.execute("""
                UPDATE client SET email=%s WHERE id=%s;
            """, (client_email, client_id,))
        if client_phone != None:
            cur.execute("""
                UPDATE client SET phone=%s WHERE id=%s;
            """, (client_phone, client_id,))
        conn.commit()

def delete_clientPhone(connect, client_id: int, client_phone: str) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DELETE FROM phone_number WHERE client_id=%s AND number=%s;
        """, (client_id, client_phone,))
        cur.execute("""
            DELETE FROM client WHERE id=%s AND phone=%s;
        """, (client_id, client_phone,))

def delete_client(connect, client_id: int) -> None:
    with connect.cursor() as cur:
        cur.execute("""
            DELETE FROM phone_number WHERE client_id=%s;
        """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE id=%s;
        """, (client_id,))
        conn.commit()

def find_client(connect, client_name: str=None, client_last_name: str=None, client_email: str=None, client_phone: str=None) -> None:
    with connect.cursor() as cur:
        if client_name != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone FROM client a
                LEFT JOIN phone_number b ON a.id=b.client_id
                WHERE a.name=%s
                GROUP BY a.id;
            """, (client_name,))
            print(cur.fetchall())
        if client_last_name != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone FROM client a
                LEFT JOIN phone_number b ON a.id=b.client_id
                WHERE a.last_name=%s
                GROUP BY a.id;
            """, (client_last_name,))
            print(cur.fetchall())
        if client_email != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone FROM client a
                LEFT JOIN phone_number b ON a.id=b.client_id
                WHERE a.email=%s
                GROUP BY a.id, b.number;
            """, (client_email,))
            print(cur.fetchall())
        if client_phone != None:
            cur.execute("""
                SELECT a.id, a.name, a.last_name, a.email, a.phone, b.number AS additional_number FROM client a, phone_number b
                WHERE a.id=b.client_id AND (a.phone=%s OR b.number=%s)
                GROUP BY a.id, b.number;
            """, (client_phone, client_phone,))
            print(cur.fetchall())

def show_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.id, a.name, a.last_name, a.email, a.phone FROM client a
            LEFT JOIN phone_number b ON a.id=b.client_id
            ORDER BY a.id;
        """)
        print(cur.fetchall())

with psycopg2.connect(database="netology_db", user="postgres", port='5431') as conn:
    create_db(conn)

    add_client(conn, 'Gleb', 'Lit', 'gleb@gmail.com', '+21')
    add_client(conn, 'Olga', 'Iv', 'olga@gmail.com', '+22')
    add_client(conn, 'Aleks', 'Bid', 'bid@gmail.com', '+23')
    add_client(conn, 'Lena', 'Bel', 'bel@gmail.com', '+24')
    add_client(conn, 'Anton', 'Var', 'var@gmail.com', '+25')
    add_client(conn, 'Toly', 'Troshin', 'toly@gmail.com', '+26')
    add_client(conn, 'Oleg', 'Osipov', 'oleg@gmail.com', '+27')

    show_db(conn)

    add_phone(conn, 1, '+31')
    add_phone(conn, 1, '+41')
    add_phone(conn, 3, '+32')
    add_phone(conn, 5, '+33')
    add_phone(conn, 7, '+34')

    find_client(conn, client_name='Toly')
    find_client(conn, client_last_name='Bel')
    find_client(conn, client_email='olga@gmail.com')
    find_client(conn, client_phone='+41')

    update_clientInfo(conn, 1, client_name='Mark', client_phone='+51')
    find_client(conn, client_phone='+51')

    delete_clientPhone(conn, 1, '+41')
    find_client(conn, client_name='Mark')

    delete_client(conn, 7)
    show_db(conn)

    drop_phone(conn)
    drop_client(conn)


