from typing import List

from django.core.exceptions import ObjectDoesNotExist
from ninja import Router, Query, PatchDict

from asset.schema import AssetOut, AssetIn, AssetSearchParams
from asset.service import AssetService
from core.schema.response import ResponseSchema, SuccessResponse, NotFoundResponse
from services.auth_jwt import JWTAuth

router = Router(tags=["Asset"], auth=JWTAuth())

service = AssetService()

@router.post('/', response={200: ResponseSchema[AssetOut]})
def create(request, payload:AssetIn):
    try:
        asset_saved = service.create(payload)
        return SuccessResponse(data=asset_saved)
    except Exception as e:
        return Exception(str(e))


@router.get('/', response={200: ResponseSchema[List[AssetOut]]})
def get(request, query: Query[AssetSearchParams]):
    try:
        assets = service.search(query)
        return SuccessResponse(data=assets)
    except Exception as e:
        return Exception(str(e))


@router.get('/{int:asset_id}', response={200: ResponseSchema[AssetOut]})
def get_by_id(request, asset_id: int):
    try:
        asset = service.repository.get_by_id(pk=asset_id)
        return SuccessResponse(data=asset)
    except Exception as e:
        return Exception(str(e))


@router.patch('/{int:asset_id}', response={200: ResponseSchema[AssetOut], 404: ResponseSchema})
def update(request, asset_id: int, payload: PatchDict[AssetIn]):
    try:
        asset_updated = service.update(asset_id, payload)
        return SuccessResponse(data=asset_updated)
    except ObjectDoesNotExist as e:
        return NotFoundResponse(message=str(e))
    except Exception as e:
        return Exception(str(e))


@router.delete("/{int:asset_id}", response={200: ResponseSchema})
def delete(request, asset_id:int):
    try:
        service.delete(asset_id)
        return SuccessResponse(message="Delete successfully")
    except ObjectDoesNotExist as e:
        return NotFoundResponse(message=str(e))