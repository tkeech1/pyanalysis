""" Blah """
from pyretriever.retriever import get_yahoo_data
from pyretriever.exception import RetrieverError
import logging
import logging.config
import argparse
import json


def main() -> None:
    with open("logging.json", "rt") as f:
        config = json.load(f)
        logging.config.dictConfig(config)
        logger = logging.getLogger("pyretriever")

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

    if args.provider == "yahoo":
        try:
            get_yahoo_data(
                provider=args.provider,
                symbols=args.symbol,
                start_date=args.start_date,
                end_date=args.end_date,
            )
            logger.debug(f"Success")
        except RetrieverError as e:
            logger.error(e)


if __name__ == "__main__":
    main()

"""

    # pull the data
    start_date: str = "2019-12-01"
    end_date: str = "2019-12-31"

    predictors: typing.Dict[str, typing.Dict[str, pd.DataFrame]] = {
        "sp500": {"ticker": "^GSPC"},
        "gdax": {"ticker": "^GDAXI"},
        "nikkei": {"ticker": "^N225"},
        "gold": {"ticker": "GLD"},
        "10y_treasury": {"ticker": "^TNX"},
    }

    for predictor in predictors:
        predictors[predictor]["data"] = data.DataReader(
            predictors[predictor]["ticker"], "yahoo", start_date, end_date
        )

    df: pd.DataFrame = None
    drop_cols: typing.List[str] = ["High", "Low", "Open", "Adj Close", "Volume"]

    for predictor in predictors:
        predictors[predictor]["data_mod"] = predictors[predictor]["data"].rename(
            columns={"Close": predictor}, errors="raise"
        )
        predictors[predictor]["data_mod"] = predictors[predictor]["data_mod"].drop(
            drop_cols, axis=1
        )
        if df is None:
            df = predictors[predictor]["data_mod"]
        else:
            df = df.join(predictors[predictor]["data_mod"], how="outer")

    df.to_csv("stock.csv")
"""
