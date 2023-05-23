import psycopg2

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR (80) NOT NULL,
            email VARCHAR(80) UNIQUE NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id_phone SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            phone VARCHAR(25) UNIQUE);
        """)


def add_new_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;", 
            (first_name, last_name, email)
        )
        result = cur.fetchone()
        return result[0]


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    data = {}
    if first_name:
        data['first_name'] = first_name
    if last_name:
        data['last_name'] = last_name
    if email:
        data['email'] = email

    with conn.cursor() as cur:
        if data:
            cond = ', '.join([f'{k}=%s' for k in data.keys()])
            values = list(data.values()) + [client_id]
            cur.execute(f'UPDATE clients SET {cond} WHERE id=%s', values)

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id=%s;", (client_id,))
        cur.execute("DELETE FROM clients WHERE id=%s;", (client_id,))


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO phones(client_id, phone) VALUES(%s, %s);",(client_id, phone))


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id=%s AND phone=%s;", (client_id, phone))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    data = {}
    if first_name:
        data['first_name'] = first_name
    if last_name:
        data['last_name'] = last_name
    if email:
        data['email'] = email
    if phone:
        data['phone'] = email
    sql = 'SELECT id, first_name, last_name, email, phone FROM clients AS c LEFT JOIN phones AS p ON p.client_id = c.id'
    if data:
        cond = ' AND '.join([f'{k}=%s' for k in data.keys()])
        sql = f'{sql} WHERE {cond}'
    with conn.cursor() as cur:
        cur.execute(sql, list(data.values()))
        return cur.fetchall()
 
   


with psycopg2.connect(database="homework5", user="elenasemenova") as conn:
    create_tables(conn)
    # client_id = add_new_client(conn, 'Elena', 'Semenova', 'elenaaaa@example.com')
    # add_phone(conn, client_id, '+79998887766')
    # add_phone(conn, client_id, '+79998887755')
    # change_client(conn, 1, last_name='Petrova', email='petrova@example.com')
    # delete_phone(conn, 6,  '+79998887766')
    # delete_client(conn, 6)
    rows = find_client(conn)
    print(rows)