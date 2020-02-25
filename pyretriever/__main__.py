""" Used to run pyretriever as a module """
from pyretriever.retriever import get_yahoo_data_async
from pyretriever.exception import RetrieverError
import logging
import logging.config
import argparse
import json
import asyncio
import typing

with open("logging.json", "rt") as f:
    config = json.load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger("pyretriever")


def get_args() -> argparse.Namespace:
    my_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Download Yahoo stock data and merge multiple "
        "ticker symbols into a single CSV file"
    )

    my_parser.add_argument(
        "--symbol",
        type=str,
        action="store",
        help="a space-separated list of symbols to download (i.e. SPY)",
        nargs="+",
    )
    my_parser.add_argument(
        "--start-date",
        type=str,
        action="store",
        help="a start date (YYYY-MM-DD)",
        required=True,
    )
    my_parser.add_argument(
        "--end-date",
        type=str,
        action="store",
        help="an end date (YYYY-MM-DD)",
        required=True,
    )
    my_parser.add_argument(
        "--provider",
        type=str,
        action="store",
        choices=["yahoo"],
        help="the data provider (yahoo is currently the only supported provider)",
        required=True,
    )

    args = my_parser.parse_args()

    logger.debug(
        f"Args: provider={args.provider}, symbols={args.symbol}, "
        + f"start_date={args.start_date}"
        + f", end_date={args.end_date}"
    )

    return args


async def main_async() -> typing.Any:

    args = get_args()
    timeout = 5

    if args.provider == "yahoo":
        try:
            task = [
                asyncio.create_task(
                    get_yahoo_data_async(
                        provider=args.provider,
                        symbols=args.symbol,
                        start_date=args.start_date,
                        end_date=args.end_date,
                        timeout=timeout,
                    )
                )
            ]
            await asyncio.wait(task, timeout=timeout)
            return task
        except RetrieverError as e:
            logger.error(e)


if __name__ == "__main__":
    task = asyncio.run(main_async())
    for t in task:
        try:
            logger.debug("Success")
            logger.debug(f"{t.result()}")
        except Exception as e:
            logger.error(e)
