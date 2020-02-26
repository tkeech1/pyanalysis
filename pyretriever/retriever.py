"""

This module retrieves data from Yahoo Finance.

Example:
    $ python -m pyretriever --symbol ^GSPC ^GDAXI --start-date 2019-12-01
        --end-date 2019-12-02 --provider=yahoo

Attributes:
        __author__ = author of the module.

        __email__ = author's email address.

        __version__ = package version.

Todo:
    * Documentation

"""
import typing
import pandas as pd
import pandas_datareader.data as data
import pyretriever.exception
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

logger = logging.getLogger(__name__)


def get_data(
    symbol: str, start_date: str, end_date: str, provider: str = "yahoo",
) -> typing.Dict[str, pd.DataFrame]:
    """Wrapper for a single call to Pandas.DataReader.

    Args:
            symbol (str): A ticker symbol available on Yahoo finance.

            start_date (str): The earliest date to return.

            end_date (str): The latest date to return.

            provider (str): The data provider to use (supports Yahoo only).

    Returns:
            Dict[str, pd.DataFrame]: A dictionary of dataframes. The key is the
                ticker symbol and the pd.Dataframe is the stock price data.

    """
    logger.debug(f"Fetching: {symbol}")
    try:
        df = data.DataReader(symbol, provider, start_date, end_date)
        logger.debug(f"Done: {symbol}")
        return {symbol: df}
    except Exception as e:
        logger.error(e)
        logger.error(
            f"Args: provider={provider}, symbol={symbol}"
            + f", start_date={start_date}"
            + f", end_date={end_date}"
        )
        raise pyretriever.exception.RetrieverError(
            " pyretriever encountered an error ", e
        )


async def get_yahoo_data_async(
    symbols: typing.List[str],
    start_date: str,
    end_date: str,
    timeout: int,
    provider: str = "yahoo",
) -> typing.Dict[str, pd.DataFrame]:
    """Gets data asynchronously from Yahoo Finance for a range of time given by
        start_date and stop_date. Supports data retrieval for multiple stock symbols.

    Args:
            symbols (List[str]): A list of ticker symbols available on Yahoo finance.

            start_date (str): The earliest date to return.

            end_date (str): The latest date to return.

            provider (str): The data provider to use (supports Yahoo only).

    Returns:
            Dict[str, pd.DataFrame]: A dictionary of dataframes in which the key is the
                ticker symbol and the pd.Dataframe is the stock price data.

    """

    if len(symbols) == 0:
        return {}

    final_dict: typing.Dict[str, pd.DataFrame] = {}

    try:

        executor = ThreadPoolExecutor(max_workers=5)
        loop = asyncio.get_event_loop()
        blocking_tasks = []

        for symbol in symbols:
            if provider == "yahoo":
                blocking_tasks.append(
                    loop.run_in_executor(
                        executor, get_data, symbol, start_date, end_date, provider
                    )
                )

        completed, pending = await asyncio.wait(blocking_tasks, timeout=timeout)
        results = [t.result() for t in completed]
        for r in results:
            for k, v in r.items():
                final_dict[k] = v

    except Exception as e:
        logger.error(e)
        logger.error(
            f"Args: provider={provider}, symbols={symbols}"
            + f", start_date={start_date}"
            + f", end_date={end_date}"
        )
        raise pyretriever.exception.RetrieverError(
            " pyretriever encountered an error ", e
        )

    return final_dict


def get_yahoo_data(
    symbols: typing.List[str], start_date: str, end_date: str, provider: str = "yahoo",
) -> typing.Dict[str, pd.DataFrame]:
    """Gets data from Yahoo Finance for a range of time given by
        start_date and stop_date. Supports data retrieval for multiple stock symbols.
    Args:
            symbols (List[str]): A list of ticker symbols available on Yahoo finance.
            start_date (str): The earliest date to return.
            end_date (str): The latest date to return.
            provider (str): The data provider to use (supports Yahoo only).
    Returns:
            Dict[str, pd.DataFrame]: A dictionary of dataframes in which the key is the
                ticker symbol and the pd.Dataframe is the stock price data.
    """

    if len(symbols) == 0:
        return {}

    symbol_data: typing.Dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        if provider == "yahoo":
            try:
                symbol_data[symbol] = get_data(
                    symbol=symbol,
                    provider=provider,
                    start_date=start_date,
                    end_date=end_date,
                )[symbol]
            except Exception as e:
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
    """Merges several data frames into a singe data frame on a given join key. This
    function renames each column to dictkey_columnname.

    Args:
        dataframes (Dict[str, pd.Dataframe]): A dictionary of dataframes
            (as returned by get_yahoo_data)

        join_column (str): The column on which to merge the dataframes

        how: The pandas df.join "how" parameter the specifies the method used to
            join the dataframes (inner, outer, etc.)

    Returns:
        pd.DataFrame: A dataframe that contains the merged dataframes.

    """
    final_df: pd.DataFrame = None
    for key, df in dataframes.items():
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
