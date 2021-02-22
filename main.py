from faker import Faker
import psycopg2


def analyze_btree(c):
    cur = c.cursor()
    cur.execute('''EXPLAIN ANALYZE SELECT * FROM customer1 WHERE name LIKE 'Den%';''')
    rows = cur.fetchall()
    for row in rows:
        print(row[0])


def analyze_hash(c):
    cur = c.cursor()# WHERE id>30000 AND id>50000
    cur.execute('''EXPLAIN ANALYZE SELECT * FROM public.customer2;''')
    rows = cur.fetchall()
    for row in rows:
        print(row[0])


def inserting(c, times=100000):
    cur = c.cursor()
    fake = Faker()
    for i in range(times):
        id = str(i)
        name = fake.name()
        add = fake.address()
        rev = fake.text()
        cur.execute(f'''
        INSERT INTO customer1(id, name, address, review)
        VALUES ('{id}','{name}','{add}','{rev}');''')
        cur.execute(f'''
        INSERT INTO customer2(id, name, address, review)
        VALUES ('{id}','{name}','{add}','{rev}');''')
        con.commit()


def create(c):
    cur = c.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS customer1
          (id INT PRIMARY KEY     NOT NULL,
          name           TEXT    NOT NULL,
          address        TEXT    NOT NULL,
          review         TEXT    NOT NULL);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS customer2
              (id INT PRIMARY KEY     NOT NULL,
              name           TEXT    NOT NULL,
              address        TEXT    NOT NULL,
              review         TEXT    NOT NULL);''')


def add_index(c):
    cur = c.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS btree_name_index ON customer1 USING btree (name);")
    c.commit()
    cur.execute("CREATE INDEX IF NOT EXISTS hash_id_index ON customer2 USING hash (id);")
    c.commit()


if __name__ == '__main__':
    con = psycopg2.connect(user="postgres", password="12345", port=5432, database="customers")
    #create(con)
    #inserting(con, times=1000000)
    #add_index(con)
    analyze_btree(con)
    print()
    analyze_hash(con)
