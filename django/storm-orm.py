from storm.locals import Store, Int, Unicode, create_database


conn = Store(create_database("postgres://postgres:postgres@127.0.0.1/test"))


class Person(object):
    __storm_table__ = 'person'
    id = Int(primary=True)
    name = Unicode()


person = Person()
person.name = 'admin'

conn.add(person)
conn.flush()

conn.find(Person, Person.name == 'admin').one()
