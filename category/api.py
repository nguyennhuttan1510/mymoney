from http.client import HTTPException

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from rest_framework.exceptions import NotFound

from category.models import Category
from typing import List
from category.schema import CategorySchema
from core.schema.response import BaseResponse, ResponseSchema
from services.auth_jwt import JWTAuth

router = Router(tags=['Category'], auth=JWTAuth())

@router.get("/", response=ResponseSchema[List[CategorySchema]])
def get_category(request):
    try:
        categories =  Category.objects.filter(Q(is_default=True) | Q(user__pk=request.user.pk))
        return BaseResponse(data=categories, message="Get all categories successfully")
    except Exception as e:
        raise HTTPException(str(e))

@router.get("/{int:category_id}", response=ResponseSchema[CategorySchema])
def get_category_by_id(request, category_id:int):
    try:
        category = Category.objects.get(Q(id=category_id) & Q(user__pk=request.user.pk))
        return BaseResponse(data=category, message="Get category by id successfully")
    except Category.DoesNotExist:
        raise NotFound(f"Category with id {category_id} not found")
    except Exception as e:
        raise HTTPException(str(e))

@router.post('/', response=ResponseSchema[CategorySchema])
def create_category(request, payload: CategorySchema):
    try:
        user = getattr(request, 'user')
        category = Category.objects.create(**payload.dict())
        category.save()
        category.user.add(user)
        return BaseResponse(data=category, message="Category created successfully")
    except Exception as e:
        raise HTTPException(str(e))

@router.delete('/{int:category_id}', response=ResponseSchema)
def delete_category(request, category_id: int):
    try:
        category = get_object_or_404(Category, Q(id=category_id) & Q(user__pk=request.user.pk))
        category.delete()
        return BaseResponse(message=f"Category with id {category_id} deleted successfully")
    except Category.DoesNotExist:
        raise NotFound(f"Category with id {category_id} not found")
    except Exception as e:
        raise HTTPException(str(e))
