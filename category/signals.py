from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def run_sql_after_migrate(sender, **kwargs):
    if sender.name != 'category':
        return

    # Đường dẫn đến file SQL
    ddl_file_path = settings.BASE_DIR / "sql/schema.sql"

    if ddl_file_path.exists():
        print(f"The path '{ddl_file_path}' exists.")
    else:
        print(f"The path '{ddl_file_path}' does not exist.")
        return False


    # Đọc và thực thi DDL
    with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
        ddl_script = ddl_file.read()

    # Thực thi DDL bằng connection
    with connection.cursor() as cursor:
        cursor.execute(ddl_script)
