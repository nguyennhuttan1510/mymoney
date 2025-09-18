from budget.models import Budget
from report.generator.wallet import TransactionReportGenerator
from report.patterns.builder import ReportBuilder
from services.http_client import NotificationAPI


class ReportService:
    @staticmethod
    def construct_report_category(builder: ReportBuilder):
        builder.set_category()
        builder.set_wallet()

    @staticmethod
    def handle_report(builder: ReportBuilder, user):
        generator = TransactionReportGenerator(builder=builder, user=user)
        file = generator.generate()
        return file

    @classmethod
    def report_by_budget(cls, budget_id: int):
        budget = Budget.objects.get(pk=budget_id)
        transactions = budget.transactions.all()

        sum_transactions = sum([transaction.amount for transaction in transactions])

        budget_transactions = {
            "budget": budget,
            "transactions": transactions,
            "spent": sum_transactions,
            "remaining": budget.amount - sum_transactions,
            "percentage_spent": (sum_transactions / budget.amount) * 100 if budget.amount > 0 else 0,
            "percentage_remaining": ((budget.amount - sum_transactions) / budget.amount) * 100 if budget.amount > 0 else 100,
        }

        cls.push_notification()

        return budget_transactions


    @staticmethod
    def push_notification():
        api = NotificationAPI()
        payload = {
            "channels": "email",
            "params": {
                "subject": "Báo cáo chi tiêu",
                "message": "Đây là báo cáo chi tiêu",
                "to_email": [
                    "nguyentan151020000@gmail.com"
                ],
                "template_name": "report",
                "content": {
                    "username": "Nguyễn Nhựt Tân",
                    "month": 8
                },
            }
        }
        try:
            res = api.post('notification/', json_data=payload)
            print('response notification', res)
        except Exception as e:
            print(e)




