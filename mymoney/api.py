from ninja import NinjaAPI
from ninja.errors import ValidationError

import asset.api
from core.exceptions.base import BusinessException
from core.exceptions.exception_handler import exception_handler, validation_exception_handler, \
    business_exception_handler
from core.exceptions.session_exception import SessionException

api = NinjaAPI()

api.add_exception_handler(BusinessException, business_exception_handler)
api.add_exception_handler(ValidationError, validation_exception_handler)
api.add_exception_handler(Exception, exception_handler)


api.add_router('/auth', 'auth.api.router')
api.add_router('/transaction', 'transaction.api.router')
api.add_router('/wallet', 'wallet.api.router')
api.add_router('/report', 'report.api.router')
api.add_router('/saving', 'saving.api.router')
api.add_router('/budget', 'budget.api.router')
api.add_router('/category', 'category.api.router')
api.add_router('/asset', 'asset.api.router')
