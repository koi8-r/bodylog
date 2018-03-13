from peewee import PostgresqlDatabase, Model, CharField


db = PostgresqlDatabase("postgres",
                        user='postgres',
                        password='postgres',
                        host='127.0.0.1')


class Person(Model):
    name = CharField()

    class Meta:
        database = db


person = Person()
person.name = 'admin'
person.save()


print(Person.select().where(Person.name == 'admin').get().id)
