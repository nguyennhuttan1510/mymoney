from http.client import HTTPException

from ninja import Router, PatchDict
from rest_framework.exceptions import NotFound

from core.schema.response import BaseResponse, ResponseSchema
from saving.models import Saving
from saving.schema import SavingSchema
from services.auth_jwt import JWTAuth

router = Router(tags=['Saving'], auth=JWTAuth())

@router.post('/', response=ResponseSchema[SavingSchema])
def create_saving(request, payload: SavingSchema):
    saving = Saving.objects.create(user=request.user, **payload.dict())
    return BaseResponse(data=saving, message='Saving created successfully')

@router.get('/{int:saving_id}', response=ResponseSchema[SavingSchema])
def get_saving(request, saving_id: int):
    try:
        saving = Saving.objects.get(user=request.user, id=saving_id)
        return BaseResponse(data=saving, message='Saving retrieved successfully')
    except Saving.DoesNotExist:
        raise NotFound('Saving not found')
    except Exception as e:
        raise HTTPException(str(e))

@router.patch('/{int:saving_id}', response=ResponseSchema[SavingSchema])
def update_saving(request, saving_id:int, item:PatchDict[SavingSchema]):
    try:
        saving = Saving.objects.get(user=request.user, id=saving_id)
        for key, value in item.items():
            if value is not None:
                setattr(saving, key, value)
        saving.save()
        return BaseResponse(data=saving, message='Saving updated successfully')
    except Saving.DoesNotExist:
        raise NotFound('Saving not found')
    except Exception as e:
        raise HTTPException(str(e))

@router.delete('/{int:saving_id}', response=ResponseSchema)
def delete_saving(request, saving_id: int):
    try:
        saving = Saving.objects.get(user=request.user, id=saving_id)
        saving.delete()
        return BaseResponse(message=f'Deleted saving {saving_id} successfully')
    except Saving.DoesNotExist:
        raise NotFound('Saving not found')