from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from marshmallow import Schema, fields, post_load
from marshmallow.validate import ValidationError, Range


class Person(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return '{:s}({id:d}, "{name:s}")'\
               .format(self.__class__.__name__,
                       **self.__dict__)


class PersonSchema(Schema):
    id = fields.Int(validate=Range(0, 65535))
    name = fields.Str(validate=lambda _: len(_) > 0, required=True)

    __model__ = Person

    @post_load()
    def unpack_person(self, data):
        return self.__model__(**data)


personSchema = PersonSchema(context={})


engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData(bind=engine)

person = Table('person', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(64), nullable=False),)


metadata.create_all()

person.delete().where(person.c.id > 0).execute()
person.insert().values([{person.c.name: _} for _
                        in ['Admin',
                            'User',
                            'Guest']])\
               .execute()

for p in person.select().execute():
    print("Selected: ({:d}: {:s})".format(*p))
    try:
        result = personSchema.load(dict(zip(('id', 'name',), p)))
    except ValidationError as e:
        print('Incorrect fields: {}'.format(', '.join(e.messages.keys())))
        raise
    else:
        print(result)
