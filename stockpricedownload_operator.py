from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from pyanalysis.retriever import get_data


class StockPriceDownloadOperator(BaseOperator):

    template_fields = ["s_date", "e_date"]

    @apply_defaults
    def __init__(
        self,
        symbol: str,
        file_location: str,
        s_date: str,
        e_date: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.file_location = file_location
        self.s_date = s_date
        self.e_date = e_date

    def execute(self, context):
        result = get_data(
            symbol=self.symbol, start_date=self.s_date, end_date=self.e_date
        )
        for k, v in result.items():
            print(f"got {k}")

        print(f"now i should save it to the disk")
