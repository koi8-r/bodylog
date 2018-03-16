from marshmallow import Schema, fields, post_load
from datetime import datetime, timezone, timedelta
from marshmallow import pprint as pp
from marshmallow.validate import ValidationError
from sys import stderr, stdout
import json


class DemoField(fields.String):
    def _serialize(self, value, attr, obj):
        assert (type(self.context) is dict)
        v = super()._serialize(value, attr, obj)
        if not v:
            return ''
        else:
            return '<{:s}>'.format(v)

    def _deserialize(self, value, attr, data):
        return super()._deserialize(value, attr, data)


class Group(object):
    def __init__(self, id, name, created=None) -> None:
        self.id = id
        self.name = name
        self.created = created or datetime.now(timezone.utc).astimezone()

    def __str__(self) -> str:
        return '{}({id}, "{name}")'.format(self.__class__.__name__, **self.__dict__)


class Person(object):
    def __init__(self, id, name, email, groups=None, created=None) -> None:
        self.id = id
        self.name = name
        self.created = created or datetime.now(timezone.utc).astimezone()
        self.email = email
        self.groups = groups

    def __str__(self) -> str:
        return '{}({id},\n' \
               '       "{name}",\n' \
               '       "{email}",\n' \
               '       [{_groups}]'.format(self.__class__.__name__,
                                           **self.__dict__,
                                           _groups=',\n        '.join(str(_) for _ in self.groups))


class GroupSchema(Schema):
    id = fields.Int(validate=lambda n: n >= 0)
    name = fields.Str()
    created = fields.DateTime()

    @post_load
    def unpack(self, data):
        return Group(**data)


class PersonSchema(Schema):
    id = fields.Int(validate=lambda n: n >= 0)
    name = DemoField()
    email = fields.Email()
    created = fields.DateTime()
    groups = fields.Nested(GroupSchema, many=True)
    friends = fields.Nested('self', many=True, exclude=('friends',))

    @post_load
    def unpack(self, data):
        return Person(**data)


person = Person(0, 'root', 'admin@localhost', groups=[Group(65535, 'nobody'), Group(10000, 'guest')])
person.friends = [Person(1000, 'user', 'user@localhost')]
personSchema = PersonSchema()
pp(personSchema.dump(person))

try:
    p = personSchema.load({'id': 65535,
                           'name': 'nobody',
                           'created': datetime.now(timezone(timedelta(0, 10800), 'MSK')).isoformat(),
                           'email': 'nobody@localhost',
                           'groups': [{'id': 65535,
                                       'name': 'nobody'},
                                      {'id': 10000,
                                       'name': 'guset'}]})
    print(p)
except ValidationError as e:
    print('Incorrect fields: ' + ', '.join(m for m in e.messages.keys()), file=stderr)
