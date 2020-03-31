from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from pyanalysis.retriever import get_data

from pathlib import Path


class StockPriceDownloadOperator(BaseOperator):

    template_fields = ["first_date", "last_date", "execution_date"]

    @apply_defaults
    def __init__(
        self,
        symbol: str,
        file_location: str,
        first_date: str,
        last_date: str,
        execution_date: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.file_location = file_location
        self.first_date = first_date
        self.last_date = last_date
        self.execution_date = execution_date

    def execute(self, context):

        file_path = f"{self.file_location}/{self.execution_date}"

        result = get_data(
            symbol=self.symbol, start_date=self.first_date, end_date=self.last_date
        )

        Path(f"{file_path}").mkdir(exist_ok=True, parents=True)

        for key, df in result.items():
            df.to_csv(f"{file_path}/{key.replace('^','')}.csv", index=False)
