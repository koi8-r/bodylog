# https://marshmallow-jsonapi.readthedocs.io/en/latest/quickstart.html#relationships

from marshmallow import Schema,fields


class Person(Schema):
    id = fields.Int()
    name = fields.Str()


person = Person()
print(person.dumps(dict(id=1,
                        name='admin'))
            .data)
