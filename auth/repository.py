from user_provider.models import UserProvider
from core.dao.repository import Repository


class UserProviderRepository(Repository[UserProvider]):
    def __init__(self):
        super().__init__(model=UserProvider)