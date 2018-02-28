class Prop(object):
    # required: Prop = Prop(required=True)

    def __init__(self, required=False):
        pass


class IntProp(Prop):
    pass


int_p = IntProp()


class ModelMeta(type):
    pass


class Model(object, metaclass=ModelMeta):
    pass


class UserModel(Model):
    #uid: IntProp.required
    uid: IntProp
    gid: int_p
    login: str
    groups: [].__class__
    n = 0
    # x: returnIntButSaveMetaOnClassLevelWithMetaclass(required=True)

    def __init__(self, uid: int, login: str):
        self.uid = uid
        self.login = login


user = UserModel(uid=0, login='root')

from pprint import pprint as pp
pp(user.__annotations__)
