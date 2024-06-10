import psycopg2

def ühenda():
    # Connect to PostgreSQL database
    # Define database connection parameters
    DB_NAME = "raamatud"
    DB_USER = "user2"
    DB_PASS = "raamatud"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    return conn, cur

def sulge(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def lisa_raamat(nimetus, autor, aasta, lk_arv, asukoht, sari=None, number=None):
    if sari == "":
        sari = None
    if number == "":
        number = None
    
    conn, cur = ühenda()
    cur.execute("SELECT * FROM lisa_raamat(%s, %s, %s, %s, %s);", (nimetus, autor, aasta, asukoht, lk_arv))
    id = cur.fetchone()
    if sari != None:
        cur.execute("CALL lisa_sari(%s, %s);", (id, sari))
    if number != None:
        cur.execute("CALL märgi_id(%s, %s);", (id, number))

    sulge(conn, cur)

def lisa_sari(nimetus):
    conn, cur = ühenda()
    cur.execute("CALL loo_sari(%s);", (nimetus, ))
    sulge(conn, cur)

def lisa_asukoht(koht):
    conn, cur = ühenda()
    cur.execute("CALL loo_asukoht(%s);", (koht, ))
    sulge(conn, cur)

def märgi_loetuks(id):
    conn, cur = ühenda()
    cur.execute("CALL märgi_loetuks(%s);", (id, ))
    
    sulge(conn, cur)

def muuda_andmed(id, asukoht, enda_id):
    conn, cur = ühenda()
    cur.execute("CALL muuda_asukoht(%s, %s);", (id, asukoht))
    if enda_id != "":
        cur.execute("CALL märgi_id(%s, %s);", (id, enda_id))
    sulge(conn, cur)

def eemalda_raamat(id):
    conn, cur = ühenda()
    cur.execute("CALL eemalda_raamat(%s);", (id, ))
    
    sulge(conn, cur)

def eemalda_asukoht(id):
    conn, cur = ühenda()
    cur.execute("CALL eemalda_asukoht(%s);", (id, ))
    sulge(conn, cur)

def täpne_otsing(nimetus=None, autor=None, aasta=None, asukoht=None, sari=None, number=None):
    conn, cur = ühenda()

    if nimetus == "":
        nimetus = None
    if autor == "":
        autor = None
    if aasta == "":
        aasta = None
    if aasta != None:
        aasta = int(aasta)
    if asukoht == "":
        asukoht = None
    if asukoht != None:
        asukoht = int(asukoht)
    if sari == "":
        sari = None
    if sari != None:
        sari = int(sari)
    if number == "":
        number = None
    if number != None:
        number = int(number)
    
    filters = {
        "name" : nimetus,
        "author" : autor,
        "release_year" : aasta,
        "location_id" : asukoht,
        "series_id" : sari,
        "id_number" : number
    }

    query = "SELECT * FROM v_kõikraamatud WHERE True"
    params = []
    for filter_name, filter_value in filters.items():
        if filter_value is not None:
            if isinstance(filter_value, str):
                query += f" AND {filter_name} ILIKE CONCAT('%%', %s, '%%')"
                params.append(filter_value)
            else:
                query += f" AND {filter_name} = %s"
                params.append(filter_value)

    cur.execute(query, tuple(params))

    results = cur.fetchall()

    sulge(conn, cur)

    return results

def kõik_raamatud():
    conn, cur = ühenda()
    cur.execute("SELECT * FROM v_raamatudnimedega;")
    data = cur.fetchall()
    sulge(conn, cur)
    return data

def asukohad():
    conn, cur = ühenda()
    cur.execute("SELECT * FROM locations;")
    result = cur.fetchall()

    sulge(conn, cur)
    return result

def sarjad():
    conn, cur = ühenda()
    cur.execute("SELECT * FROM series;")
    result = cur.fetchall()
    sulge(conn, cur)
    return result