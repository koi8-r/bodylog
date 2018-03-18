from marshmallow import Schema, fields, post_load, post_dump, validates_schema
from marshmallow import pprint as pp
from marshmallow.validate import ValidationError, Range


class Person(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name


class PersonSchema(Schema):
    id = fields.Int(validate=Range(0, 65535))
    name = fields.Str(validate=lambda _: len(_) > 0, required=True)

    __model__ = Person

    @validates_schema()
    def validate_schema(self, data):
        if not data['name']:
            raise ValidationError('Incorrect name')

    @post_dump
    def pack_person(self, data):
        pp(super().validate(data))  # maybe correct direct field validation call during serialization

        if not data['name']:
            raise ValidationError('Incorrect name', ['name'])
        else:
            return data

    @post_load()
    def unpack_person(self, data):
        return self.__model__(**data)


personSchema = PersonSchema(context={})
try:
    result = personSchema.load({'id': 0, 'name': 'root'})
    pp(personSchema.dump(Person(1000, 'root')))
except ValidationError as e:
    print('Incorrect fields: {}'.format(', '.join(e.messages.keys())))
else:
    pp(result)
