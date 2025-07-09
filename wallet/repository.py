from django.db.models import Q
from ninja import Query
from utils.query_builder import Specification, QueryBuilder
from utils.repository import Repository
from wallet.models import Wallet
from wallet.schema import WalletParam


class WalletSpecification(Specification[Wallet]):
    def __init__(self, params: Query[WalletParam]):
        self.params = params
        self.builder = QueryBuilder()

    def is_satisfied(self) -> Q:
        params_dict = self.params.model_dump(exclude_unset=True)
        self.base_query(params_dict, builder=self.builder)
        return self.builder.build()


class WalletRepository(Repository):
    def __init__(self):
        super().__init__(model=Wallet)

    def search(self, params: Query[WalletParam]):
        specification = WalletSpecification(params)
        return self.filter(specification)

    def check_existed(self, wallet_name: str, user_id: int):
        return self.model.objects.filter(name=wallet_name, user_id=user_id).exists()

