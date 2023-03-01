from extensions import marshmallow as ma
from marshmallow import pre_load, post_dump, SchemaOpts, Schema


class BaseSchemaOpts(SchemaOpts):

    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.name = getattr(self, 'name', None)
        self.plural_name = str(self.name)+'s'


class BaseSchema(Schema):
    name = 'base'

    @pre_load(pass_many=True)
    def pre_load(self, data, many, **kwargs):
        key = str(self.name) + 's' if many else self.name
        return data[key]

    @post_dump(pass_many=True)
    def post_dump(self, data, many, **kwargs):
        key = str(self.name) + 's' if many else self.name
        return {key: data}
