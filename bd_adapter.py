import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker

import logins



conn = psycopg2.connect(dbname=logins.DBNAME, user=logins.LOGIN, password=logins.PASS)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS my_table")
cur.execute("DROP TABLE IF EXISTS my_trafic")

conn.commit()

cur.execute("CREATE TABLE my_table (my_id serial PRIMARY KEY, name varchar, power int);")
cur.execute("INSERT INTO my_table (name, power) VALUES (%s, %s)", ("Serg", 12))
cur.execute("INSERT INTO my_table (name, power) VALUES (%s, %s)", ("Andr", 11))
cur.execute("INSERT INTO my_table (name, power) VALUES (%s, %s)", ("Ileg", 15))
conn.commit()

cur.execute("SELECT * from my_table")
one_line = cur.fetchone()
print(one_line)


full = cur.fetchall()
print(full)
cur.close()
conn.close()

with psycopg2.connect(dbname=logins.DBNAME, user=logins.LOGIN, password=logins.PASS) as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        execute_values(cur, "INSERT INTO my_table (name, power) VALUES %s", [("Jan", 18),("Ino", 19)])

        cur.execute("SELECT * from my_table")
        records = cur.fetchall()
        print(records)
        print(records[0]['name'])

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+logins.LOGIN+':'+logins.PASS+'@localhost:5432/'+logins.DBNAME)


with engine.connect() as connection:
    result = connection.execute("SELECT * from products")
    for elem in result:
        print(elem)

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'

    my_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    power = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_name = MyTable(name='Frodo', power=7)
session.add(new_name)
session.commit()



for elem in session.query(MyTable).order_by(MyTable.power):
    print(elem.name, elem.power)




















