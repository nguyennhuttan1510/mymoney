from http.client import HTTPException
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from ninja import Router, Query, PatchDict
from rest_framework.exceptions import NotFound

from budget.schema import BudgetOut, BudgetIn, BudgetParam, BudgetUpdate
from budget.service import BudgetService
from core.exceptions.exceptions import ValidateError
from core.schema.response import ResponseSchema, CreateSuccessResponse, SuccessResponse
from services.auth_jwt import JWTAuth
from django.db import transaction as transaction_db

router = Router(tags=['Budget'], auth=JWTAuth())


@router.post("/", response={201: ResponseSchema[BudgetOut], 400: ResponseSchema})
def create_budget(request, payload: BudgetIn):
    try:
        instance = BudgetService.create_budget(payload=payload)
        return CreateSuccessResponse(data=instance, message="Create budget successfully")
    except ValueError as e:
        raise ValidateError(str(e))
    except Exception as e:
        print('e', e)
        raise HTTPException(str(e))


@router.get("/", response={200: ResponseSchema[List[BudgetOut]], 422: ResponseSchema})
def get_budgets(request, filters: Query[BudgetParam]):
    try:
        budgets = BudgetService.get_all_budget_for_user(user_id=request.auth.pk, **filters.dict(exclude_unset=True))
        return SuccessResponse(data=budgets, message='Get budgets success')
    except Exception as e:
        raise HTTPException(str(e))


@router.get("/{int:budget_id}", response={200: ResponseSchema[BudgetOut], 422: ResponseSchema})
def get_budget(request, budget_id: int):
    try:
        budget = BudgetService.get_budget(budget_id=budget_id, user_id=request.auth.pk)
        return SuccessResponse(data=budget, message="Get budget successfully")

    except ObjectDoesNotExist:
        raise NotFound(f"Budget with id {budget_id} does not exist")
    except Exception as e:
        raise HTTPException(str(e))


@router.patch("/{int:budget_id}", response={200: ResponseSchema[BudgetOut], 422: ResponseSchema})
def update_budget(request, budget_id: int, payload: BudgetUpdate):
    try:
        budget_updated = BudgetService.update_budget(budget_id=budget_id, user_id=request.auth.pk, payload=payload)
        return SuccessResponse(data=budget_updated, message=f"Update budget {budget_id} successfully")
    except ObjectDoesNotExist:
        raise NotFound(f"Budget with id {budget_id} does not exist")
    except ValueError as e:
        raise ValidateError(str(e))
    except Exception as e:
        raise HTTPException(str(e))


@router.delete("/{int:budget_id}", response=ResponseSchema)
def delete_budget(request, budget_id: int):
    try:
        BudgetService.delete_budget(budget_id=budget_id, user_id=request.auth.pk)
        return SuccessResponse(message=f"Delete budget {budget_id} successfully")
    except ObjectDoesNotExist:
        raise NotFound(f'Not found budget {budget_id}')
    except Exception as e:
        raise HTTPException(str(e))
