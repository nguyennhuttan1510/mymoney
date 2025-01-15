from ninja import ModelSchema

from saving.models import Saving


class SavingSchema(ModelSchema):
    class Meta:
        model = Saving
        fields = ['id', 'name', 'target_amount', 'current_amount', 'deadline']