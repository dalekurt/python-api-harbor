# server/app/tasks/scheduled_tasks.py
from server.app.databases.celery import celery_app
from server.app.workflows.exchangerates_workflow import FetchTranslateStoreWorkflowImpl


@celery_app.task
def fetch_weather_data():
    workflow = FetchTranslateStoreWorkflowImpl()
    workflow.start_process("weather")


@celery_app.task
def fetch_exchange_rates_data():
    workflow = FetchTranslateStoreWorkflowImpl()
    workflow.start_process("exchangerates")
