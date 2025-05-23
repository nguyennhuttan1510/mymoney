from http.client import HTTPException

from django.db.models import Q
from ninja import Router
from rest_framework.exceptions import NotFound

from budget.models import Budget
from budget.schema import BudgetSchema, BudgetCreateSchema
from category.models import Category
from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth

router = Router(tags=['Budget'], auth=JWTAuth())

@router.get("/{int:budget_id}", response=ResponseSchema[BudgetSchema])
def get_budget(request, budget_id:int):
    try:
        budget = Budget.objects.get(Q(id=budget_id) & Q(user__pk=request.user.pk))
        return Response(data=budget, message="Get budget successfully")

    except Budget.DoesNotExist:
        raise NotFound(f"Budget with id {budget_id} does not exist")
    except Exception as e:
        raise HTTPException(str(e))


@router.post("/", response=ResponseSchema[BudgetSchema])
def create_budget(request, payload: BudgetCreateSchema):
    try:
        category = Category.objects.get(id=payload.category)
        budget_data = {**payload.dict(), "category": category}
        budget = Budget.objects.create(user=request.user, **budget_data)
        return Response(data=budget, message="Create budget successfully")
    except Category.DoesNotExist:
        raise NotFound("Category not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.delete("/{int:budget_id}", response=ResponseSchema)
def delete_budget(request, budget_id: int):
    try:
        budget = Budget.objects.get(Q(id=budget_id) & Q(user__pk=request.user.pk))
        budget.delete()
        return Response(message=f"Delete budget {budget_id} successfully")
    except Budget.DoesNotExist:
        raise NotFound(f'Not found budget {budget_id}')
