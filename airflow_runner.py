from airflow import DAG
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from operators.hello_operator import HelloOperator
from operators.stockpricedownload_operator import StockPriceDownloadOperator
from pyanalysis.retriever import get_yahoo_data
from datetime import datetime, timedelta

default_args = {
    "owner": "tk",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["tkeech1@hotmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    "execution_timeout": timedelta(seconds=60),
    "history": 2,
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    "pyanalysis",
    default_args=default_args,
    description="A simple DAG for getting stock prices",
    schedule_interval=timedelta(days=1),
)

stock_list = ["^GSPC", "^GDAXI", "SPY", "GOOG"]
file_location = "~/stock_data/"

# end date is the current day
end_date = """{{ds}}"""
# start date is the current day minus 7 days (set by the params.history values for each task)
# execution_date is a datetime object whereas ds is just a timestamp str
# start_date = """{{ (
#    execution_date - macros.timedelta(days=params.history)
# ).strftime("%Y-%m-%d") }}"""

# params.history doesn't seem to work correctly in a custom operator
start_date = """{{ (
    execution_date - macros.timedelta(days=2)
).strftime("%Y-%m-%d") }}"""


op_list = {}
for stock in stock_list:

    # download_spy = PythonOperator(
    #    task_id=f"download_prices_{stock}",
    #    provide_context=False,
    #    python_callable=get_yahoo_data,
    #    op_kwargs={"symbols": [stock], "start_date": start_date, "end_date": end_date,},
    #    params={"history": 7},
    #    dag=dag,
    # )

    op_list[stock] = StockPriceDownloadOperator(
        task_id=f"{stock.replace('^','')}",
        symbol=stock,
        file_location=file_location,
        s_date=start_date,
        e_date=end_date,
        dag=dag,
    )

# op1..n = download files, place in date folder, name SYMBOL.csv
# op_merge = merge files, read date folder, create dict str->dataframe, call merge, save merged csv
# op_store = upload merged CSV to AWS
