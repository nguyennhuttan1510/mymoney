from ninja import Schema, ModelSchema

from category.models import Category


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']