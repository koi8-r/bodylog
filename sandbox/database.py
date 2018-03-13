from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select
from pprint import pprint as pp


metadata = MetaData()
person = Table('person', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(256), nullable=False),)

address = Table('address', metadata,
                Column('id', Integer, primary_key=True),
                Column('person_id', None, ForeignKey(person.c.id)),
                Column('address', String(1024), nullable=False),)


engine = create_engine('postgresql://postgres:postgres@127.0.0.1/test', echo=True)
metadata.create_all(engine)


assert person.primary_key.columns['id'] == person.c.id  # is


print(insert(person))
print(select([person]))
print(person.select())
print(person.insert())
print(person.insert().values(name='admin').compile().params)
ins = person.insert().values(name='admin')
ins.bind = engine
print(ins)
sql = engine.connect()

print(sql.execute(person.insert().values(name='admin')).inserted_primary_key)
print(sql.execute(person.insert(), name='user').inserted_primary_key)
print(person.c.id == 'admin')


print([ r for r in sql.execute(select([person, address]))])

print((person.c.name + 'istrator').compile(bind=engine))
# print((person.c.name + 'istrator').compile(bind=create_engine('mysql://')))
print((person.c.name.op('&')(0xff)))  # type_coerce, bool_op
