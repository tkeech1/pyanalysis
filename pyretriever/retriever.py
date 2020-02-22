""" docstring """
import typing
import pandas as pd
import pandas_datareader.data as data
import pyretriever.exception
import logging

logger = logging.getLogger(__name__)


def get_yahoo_data(
    symbols: typing.List[str], start_date: str, end_date: str, provider: str = "yahoo",
) -> typing.Dict[str, pd.DataFrame]:
    """docstring"""

    symbol_data: typing.Dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        if provider == "yahoo":
            try:
                symbol_data[symbol] = data.DataReader(
                    symbol, provider, start_date, end_date
                )
            except Exception as e:
                # except pandas_datareader.exceptions. as e:
                logger.error(e)
                logger.error(
                    f"Args: provider={provider}, symbols={symbols}"
                    + f", start_date={start_date}"
                    + f", end_date={end_date}"
                )
                raise pyretriever.exception.RetrieverError(
                    " pyretriever encountered an error ", e
                )

    return symbol_data


def merge_dataframes(
    dataframes: typing.Dict[str, pd.DataFrame], join_column: str, how: str
) -> pd.DataFrame:
    """docstring"""
    final_df: pd.DataFrame = None
    for key, df in dataframes.items():
        # TODO make this a comprehension
        column_dict = {}
        for col in df.columns:
            if join_column == col:
                continue
            column_dict[col] = f"{key}_{col}"

        df = df.rename(columns=column_dict, errors="raise")
        if final_df is None:
            final_df = df
        else:
            final_df = final_df.join(df, how=how, rsuffix=f"_{key}")
            final_df = final_df.drop(columns=f"{join_column}_{key}")

    return final_df
