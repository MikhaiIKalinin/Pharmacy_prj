import psycopg2
from psycopg2 import sql, errors
from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] executed in {(end - start) * 1000:.2f} ms")
        return res
    return wrapper

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port=5432
        )

    def close(self):
        self.conn.close()

    # ---------- HELPERS ----------
    def fetch_query(self, query, params=None, fetch_all=True):
        cur = self.conn.cursor()
        try:
            cur.execute(query, params or ())
            rows = cur.fetchall() if fetch_all else cur.fetchmany(50)
            cur.close()
            return rows
        except Exception as e:
            cur.close()
            print("Error fetch_query:", e)
            return []

    def execute_query(self, query, params=None):
        cur = self.conn.cursor()
        try:
            cur.execute(query, params or ())
            self.conn.commit()
            cur.close()
            return "OK"
        except errors.ForeignKeyViolation as e:
            self.conn.rollback()
            cur.close()
            return "FK_ERROR" # Повертаємо спеціальний код помилки
        except Exception as e:
            self.conn.rollback()
            cur.close()
            print("Error execute_query:", e)
            return str(e)

    # ---------- READ ----------
    @timeit
    def get_pharmacies_limited(self):
        return self.fetch_query('SELECT "Id", "Name", "Adress" FROM "Pharmacies" ORDER BY "Id" LIMIT 50')

    @timeit
    def get_pharmacies(self):
        return self.fetch_query('SELECT "Id", "Name", "Adress" FROM "Pharmacies" ORDER BY "Id"')

    @timeit
    def get_pharmacy_by_id(self, id_val):
        return self.fetch_query('SELECT "Id", "Name", "Adress" FROM "Pharmacies" WHERE "Id"=%s', (id_val,))

    @timeit
    def get_phonetypes(self):
        return self.fetch_query('SELECT "Id", "Name" FROM "PhoneTypes" ORDER BY "Id"')

    @timeit
    def get_phones(self):
        return self.fetch_query('SELECT "Id", "Name", "PharmacyId", "PhoneTypeId" FROM "Phones" ORDER BY "Id"')

    @timeit
    def get_manufacturers(self):
        return self.fetch_query('SELECT "Id", "Name" FROM "Manufacturers" ORDER BY "Id"')

    @timeit
    def get_drugs(self):
        return self.fetch_query('SELECT "Id", "Name", "ManufacturerId", "Price" FROM "Drugs" ORDER BY "Id"')

    @timeit
    def get_availabilities(self):
        return self.fetch_query('SELECT "PharmacyId", "DrugId", "Quantity", "UpdatedAt" FROM "Availabilities" ORDER BY "PharmacyId", "DrugId"')

    # ---------- ADD ----------
    @timeit
    def add_pharmacy(self, name, adress):
        # Отримати максимальний Id
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Pharmacies"'
        rows = self.fetch_query(max_id_query)
        next_id = rows[0][0] + 1 if rows else 1

        return self.execute_query(
            'INSERT INTO "Pharmacies" ("Id", "Name", "Adress") OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s)',
            (next_id, name, adress)
        )

    @timeit
    def add_phonetype(self, name):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "PhoneTypes"'
        rows = self.fetch_query(max_id_query)
        next_id = rows[0][0] + 1 if rows else 1

        return self.execute_query(
            'INSERT INTO "PhoneTypes" ("Id", "Name") OVERRIDING SYSTEM VALUE VALUES (%s, %s)',
            (next_id, name)
        )

    @timeit
    def add_phone(self, name, pharmacyid, phonetypeid):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Phones"'
        rows = self.fetch_query(max_id_query)
        next_id = rows[0][0] + 1 if rows else 1

        return self.execute_query(
            'INSERT INTO "Phones" ("Id", "Name", "PharmacyId", "PhoneTypeId") OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s)',
            (next_id, name, pharmacyid, phonetypeid)
        )

    @timeit
    def add_manufacturer(self, name):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Manufacturers"'
        rows = self.fetch_query(max_id_query)
        next_id = rows[0][0] + 1 if rows else 1

        return self.execute_query(
            'INSERT INTO "Manufacturers" ("Id", "Name") OVERRIDING SYSTEM VALUE VALUES (%s, %s)',
            (next_id, name)
        )

    @timeit
    def add_drug(self, name, manufactureid, price):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Drugs"'
        rows = self.fetch_query(max_id_query)
        next_id = rows[0][0] + 1 if rows else 1

        # ВИПРАВЛЕННЯ
        return self.execute_query(
            'INSERT INTO "Drugs" ("Id", "Name", "ManufacturerId", "Price") OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s)',
            (next_id, name, manufactureid, price)
        )

    @timeit
    def add_availability(self, pharmacyid, drugid, quantity):
        return self.execute_query(
            'INSERT INTO "Availabilities" ("PharmacyId", "DrugId", "Quantity", "UpdatedAt") VALUES (%s, %s, %s, now())',
            (pharmacyid, drugid, quantity)
        )

    # ---------- SEARCH & ANALYTICS ----------
    @timeit
    def search_drug_stats(self, min_price, max_price, name_pattern):
        query = """
                SELECT d."Name", m."Name", d."Price"
                FROM "Drugs" d
                         JOIN "Manufacturers" m ON d."ManufacturerId" = m."Id"
                WHERE d."Price" BETWEEN %s AND %s
                  AND d."Name" LIKE %s
                ORDER BY d."Price" DESC \
                """
        return self.fetch_query(query, (min_price, max_price, f"%{name_pattern}%"))

    @timeit
    def search_pharmacy_stock(self, drug_name_part, min_qty):
        query = """
                SELECT p."Name", d."Name", a."Quantity"
                FROM "Availabilities" a
                         JOIN "Pharmacies" p ON a."PharmacyId" = p."Id"
                         JOIN "Drugs" d ON a."DrugId" = d."Id"
                WHERE d."Name" LIKE %s \
                  AND a."Quantity" >= %s
                ORDER BY a."Quantity" DESC \
                """
        return self.fetch_query(query, (f"%{drug_name_part}%", min_qty))

    @timeit
    def search_updates_by_date(self, start_date, end_date):
        query = """
                SELECT p."Name", count(a."DrugId") as UpdatedCount
                FROM "Availabilities" a
                         JOIN "Pharmacies" p ON a."PharmacyId" = p."Id"
                WHERE a."UpdatedAt" BETWEEN %s AND %s
                GROUP BY p."Name"
                ORDER BY UpdatedCount DESC \
                """
        return self.fetch_query(query, (start_date, end_date))

    # ---------- UPDATE ----------
    @timeit
    def update_pharmacy(self, id_, name, adress):
        return self.execute_query('UPDATE "Pharmacies" SET "Name"=%s, "Adress"=%s WHERE "Id"=%s', (name, adress, id_))

    @timeit
    def update_phonetype(self, id_, name):
        return self.execute_query('UPDATE "PhoneTypes" SET "Name"=%s WHERE "Id"=%s', (name, id_))

    @timeit
    def update_phone(self, id_, name, pharmacyid, phonetypeid):
        return self.execute_query('UPDATE "Phones" SET "Name"=%s, "PharmacyId"=%s, "PhoneTypeId"=%s WHERE "Id"=%s', (name, pharmacyid, phonetypeid, id_))

    @timeit
    def update_manufacturer(self, id_, name):
        return self.execute_query('UPDATE "Manufacturers" SET "Name"=%s WHERE "Id"=%s', (name, id_))

    @timeit
    def update_drug(self, id_, name, manufactureid, price):
        return self.execute_query('UPDATE "Drugs" SET "Name"=%s, "ManufactureId"=%s, "Price"=%s WHERE "Id"=%s', (name, manufactureid, price, id_))

    @timeit
    def update_availability(self, pharmacyid, drugid, quantity):
        return self.execute_query('UPDATE "Availabilities" SET "Quantity"=%s, "UpdatedAt"=now() WHERE "PharmacyId"=%s AND "DrugId"=%s', (quantity, pharmacyid, drugid))

    # ---------- DELETE ----------
    @timeit
    def delete_by_id(self, table, id_field, id_value):
        q = sql.SQL('DELETE FROM {} WHERE {} = %s').format(sql.Identifier(table), sql.Identifier(id_field))
        cur = self.conn.cursor()
        try:
            cur.execute(q, (id_value,))

            rows_deleted = cur.rowcount

            self.conn.commit()
            cur.close()

            if rows_deleted == 0:
                return "NOT_FOUND"
            return "OK"

        except errors.ForeignKeyViolation:
            self.conn.rollback()
            cur.close()
            return "FK_ERROR"
        except Exception as e:
            self.conn.rollback()
            cur.close()
            return str(e)

    @timeit
    def delete_availability(self, pharmacyid, drugid):
        return self.execute_query('DELETE FROM "Availabilities" WHERE "PharmacyId"=%s AND "DrugId"=%s', (pharmacyid, drugid))

    # ---------- GENERATION ----------
    @timeit
    def ensure_default_phonetypes(self):
        # insert basic phone types if table empty
        rows = self.fetch_query('SELECT count(*) FROM "PhoneTypes"')
        if rows and rows[0][0] == 0:
            types = ['mobile', 'landline', 'fax']
            for t in types:
                self.execute_query('INSERT INTO "PhoneTypes" ("Name") VALUES (%s)', (t,))
            print("Default PhoneTypes inserted.")
        else:
            print("PhoneTypes not empty, skipped.")

    @timeit
    def generate_pharmacies(self, n):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Pharmacies"'
        rows = self.fetch_query(max_id_query)
        start_id = rows[0][0] + 1 if rows else 1

        q = f"""
        INSERT INTO "Pharmacies" ("Id", "Name", "Adress")
        OVERRIDING SYSTEM VALUE
        SELECT 
            {start_id} + gs - 1,
            'Pharmacy_' || gs,
            'Address ' || gs
        FROM generate_series(1, {int(n)}) AS gs;
        """
        return self.execute_query(q)

    @timeit
    def generate_manufacturers(self, n):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Manufacturers"'
        rows = self.fetch_query(max_id_query)
        start_id = rows[0][0] + 1 if rows else 1

        q = f"""
        INSERT INTO "Manufacturers" ("Id", "Name")
        SELECT 
            {start_id} + gs - 1,
            'Manufacturer_' || gs
        FROM generate_series(1, {int(n)}) AS gs;
        """
        return self.execute_query(q)

    def generate_drugs(self, n):
        query = f"""
            WITH max_id AS (
                SELECT COALESCE(MAX("Id"), 0) AS start_id FROM "Drugs"
            ),
            generated AS (
                SELECT
                    (ROW_NUMBER() OVER () + (SELECT start_id FROM max_id)) AS "Id",
                    'Drug_' || (ROW_NUMBER() OVER ()) AS "Name",
                    (SELECT "Id" FROM "Manufacturers" ORDER BY random() LIMIT 1) AS "ManufacturerId",
                    round((random() * 200)::numeric, 2) AS "Price"
                FROM generate_series(1, {n})
            )
            INSERT INTO "Drugs" ("Id", "Name", "ManufacturerId", "Price")
            SELECT "Id", "Name", "ManufacturerId", "Price" FROM generated;
        """
        self.execute_query(query)

    @timeit
    def generate_phones(self, n):
        max_id_query = 'SELECT COALESCE(MAX("Id"), 0) FROM "Phones"'
        rows = self.fetch_query(max_id_query)
        start_id = rows[0][0] + 1 if rows else 1

        q = f"""
        INSERT INTO "Phones" ("Id", "Name", "PharmacyId", "PhoneTypeId")
        SELECT 
            {start_id} + gs - 1,
            'Phone_' || gs,
            ph.ids[1 + floor(random() * array_length(ph.ids, 1))::int],
            pt.ids[1 + floor(random() * array_length(pt.ids, 1))::int]
        FROM generate_series(1, {int(n)}) AS gs
        CROSS JOIN (SELECT array_agg("Id") as ids FROM "Pharmacies") ph
        CROSS JOIN (SELECT array_agg("Id") as ids FROM "PhoneTypes") pt;
        """
        return self.execute_query(q)

    @timeit
    def generate_availabilities(self, n):
        """Генерує або оновлює записи про наявність"""
        q = f"""
        INSERT INTO "Availabilities" ("PharmacyId", "DrugId", "Quantity", "UpdatedAt")
        SELECT 
            p."Id", 
            d."Id", 
            (floor(random()*100)::int + 1), 
            now()
        FROM (SELECT "Id" FROM "Pharmacies" ORDER BY random() LIMIT {int(n)}) p,
             (SELECT "Id" FROM "Drugs" ORDER BY random() LIMIT {int(n)}) d
        LIMIT {int(n)}
        ON CONFLICT ("PharmacyId", "DrugId") 
        DO UPDATE SET 
            "Quantity" = EXCLUDED."Quantity",
            "UpdatedAt" = EXCLUDED."UpdatedAt";
        """
        return self.execute_query(q)