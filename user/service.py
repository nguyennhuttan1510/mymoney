from django.db.models import Sum, Count

from asset.repository import AssetRepository
from asset.schema import AssetSearchParams
from asset.service import AssetService
from budget.repository import BudgetRepository
from budget.schema import BudgetParam, BudgetQueryParam, BudgetListOut
from wallet.repository import WalletRepository
from wallet.schema import WalletParam, WalletListOut


class UserService:

    @classmethod
    def get_wallets(cls, user_id:int) -> WalletListOut:
        repository = WalletRepository()
        qs = repository.search(params=WalletParam(user=user_id))
        aggregates = qs.aggregate(
            total=Sum('balance'),
            count=Count('id')
        )
        return WalletListOut(
            total = aggregates['total'] or 0,
            count = aggregates['count'] or 0,
            data = list(qs)
        )


    @classmethod
    def get_budgets(cls, user_id:int) -> BudgetListOut:
        repository = BudgetRepository()
        qs = repository.search(params=BudgetQueryParam(user_id=user_id))
        aggregates = qs.aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        return BudgetListOut(
            total = aggregates['total'] or 0,
            count = aggregates['count'] or 0,
            data = list(qs)
        ).model_dump(by_alias=True)


    @classmethod
    def get_assets(cls, user_id:int):
        service = AssetService()
        return service.asset_list(AssetSearchParams(user_id=user_id))
