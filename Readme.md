deploy: uvicorn mymoney.asgi:application --workers 4
load data: python -X utf-8 manage.py loaddata data.json  