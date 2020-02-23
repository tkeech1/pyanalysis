""" Tests for pyretriever """
import typing
from pyretriever.retriever import get_yahoo_data, merge_dataframes
from pyretriever.exception import RetrieverError
from unittest.mock import patch
import pandas as pd
import pytest


@patch("pandas_datareader.data.DataReader")
def test_get_yahoo_data(mock_DataReader):

    test_cases: list[typing.Any] = [
        # test empty symbol list
        {
            "symbols": [],
            "provider": "yahoo",
            "start_date": None,
            "end_date": None,
            "mock_return": pd.DataFrame(),
            "expected_return": {},
        },
        # test multiple symbols
        {
            "symbols": ["SPY", "QQQ"],
            "provider": "yahoo",
            "start_date": "2019-12-01",
            "end_date": "2019-12-02",
            "mock_return": pd.DataFrame({"ZZZ": [1, 2]}),
            "expected_return": {
                "SPY": pd.DataFrame({"ZZZ": [1, 2]}),
                "QQQ": pd.DataFrame({"ZZZ": [1, 2]}),
            },
        },
        # test a single symbol
        {
            "symbols": ["PPP"],
            "start_date": "2019-12-01",
            "end_date": "2019-12-02",
            "provider": "yahoo",
            "mock_return": pd.DataFrame({"AAA": [1, 2]}),
            "expected_return": {"PPP": pd.DataFrame({"AAA": [1, 2]})},
        },
    ]

    for test_case in test_cases:
        mock_DataReader.return_value = test_case["mock_return"]

        actual_value = get_yahoo_data(
            symbols=test_case["symbols"],
            start_date=test_case["start_date"],
            end_date=test_case["end_date"],
            provider=test_case["provider"],
        )

        # test that the mock was called for each symbol
        for symbol in test_case["symbols"]:
            mock_DataReader.assert_any_call(
                symbol, "yahoo", test_case["start_date"], test_case["end_date"],
            )

        # test that the returned dict has an item for each symbol
        assert test_case["expected_return"].keys() == actual_value.keys()

        # test that the returned data frame matches the expected frame
        for key, df in actual_value.items():
            assert df.columns == actual_value[key].columns


@patch("pandas_datareader.data.DataReader")
def test_get_yahoo_data_exception(mock_DataReader):

    test_cases: list[typing.Any] = [
        # test exception
        {
            "symbols": ["GSPC"],
            "provider": "yahoo",
            "start_date": None,
            "end_date": None,
            "mock_side_effect": Exception("Boom!"),
            "expected_exception": RetrieverError,
        }
    ]

    for test_case in test_cases:
        mock_DataReader.side_effect = test_case["mock_side_effect"]

        with pytest.raises(Exception) as exception_info:
            get_yahoo_data(
                symbols=test_case["symbols"],
                start_date=test_case["start_date"],
                end_date=test_case["end_date"],
                provider=test_case["provider"],
            )

        assert isinstance(exception_info.value, test_case["expected_exception"])


def test_merge_data():

    test_cases: list[typing.Any] = [
        # test one column
        {
            "input": {
                "SPY": pd.DataFrame({"Date": ["01-01-2001", "01-02-2001"]}),
                "QQQ": pd.DataFrame(
                    {"Date": ["01-01-2001", "01-02-2001"], "High": [3, 4]}
                ),
            },
            "join_column": "Date",
            "how": "outer",
            "expected_output_columns": ["Date", "QQQ_High"],
            "expected_rows": 2,
        },
        # test multiple column
        {
            "input": {
                "SPY": pd.DataFrame(
                    {
                        "Date": ["01-01-2001", "01-02-2001"],
                        "High": [3, 4],
                        "Low": [3, 4],
                    }
                ),
                "QQQ": pd.DataFrame(
                    {"Date": ["01-01-2001", "01-02-2001"], "Low": [None, 4]}
                ),
                "INX": pd.DataFrame(
                    {"Date": ["01-01-2001", "01-02-2001"], "High": [3, 4]}
                ),
                "GSPC": pd.DataFrame(
                    {"Date": ["01-01-2001", "01-02-2001"], "Close": [3, None]}
                ),
                "GOOG": pd.DataFrame(
                    {
                        "Date": [
                            "01-01-2001",
                            "01-02-2001",
                            "01-03-2001",
                            "01-04-2001",
                        ],
                        "Adj Close": [3, 4, None, 6],
                    }
                ),
            },
            "join_column": "Date",
            "how": "outer",
            "expected_output_columns": [
                "Date",
                "SPY_High",
                "SPY_Low",
                "QQQ_Low",
                "INX_High",
                "GSPC_Close",
                "GOOG_Adj Close",
            ],
            "expected_rows": 4,
        },
    ]

    for test_case in test_cases:

        df = merge_dataframes(
            test_case["input"], test_case["join_column"], test_case["how"]
        )
        assert list(df.columns) == test_case["expected_output_columns"]
        assert len(df.index) == test_case["expected_rows"]
