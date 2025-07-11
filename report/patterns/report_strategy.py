from abc import ABC

class BaseReportStrategy(ABC):
    def __init__(self, user):
        self.user = user

    def generate(self):
        """Return file generated excel"""
        pass
