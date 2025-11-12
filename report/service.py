from budget.models import Budget
from report.generator.wallet import TransactionReportGenerator
from report.patterns.builder import ReportBuilder
from services.http_client import NotificationAPI


class ReportService:

    @staticmethod
    def handle_report(builder: ReportBuilder, user):
        generator = TransactionReportGenerator(builder=builder, user=user)
        file = generator.generate()
        return file


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




