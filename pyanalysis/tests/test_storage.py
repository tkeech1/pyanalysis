""" Tests for pyanalysis """
import typing
from pyanalysis.storage import StorageError, df_to_s3_csv
from unittest.mock import patch, MagicMock
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def df_to_s3_csv_test_cases():
    test_cases: typing.List[typing.Any] = [
        {
            "bucket_name": "mybucket",
            "file_name": "myfile",
            "df": pd.DataFrame(
                {"High": [3, 4], "Low": [3, 4]}, index=["01-01-2001", "01-02-2001"],
            ),
            "response": {
                "Expiration": "string",
                "ETag": "string",
                "ServerSideEncryption": "AES256",
                "VersionId": "string",
                "SSECustomerAlgorithm": "string",
                "SSECustomerKeyMD5": "string",
                "SSEKMSKeyId": "string",
                "SSEKMSEncryptionContext": "string",
                "RequestCharged": "requester",
            },
        }
    ]
    yield test_cases
    # tear-down


@patch("boto3.resource")
def test_df_to_s3_csv(mock_boto3, df_to_s3_csv_test_cases):

    for test_case in df_to_s3_csv_test_cases:
        mock_boto3_object = MagicMock()
        mock_boto3_object.Object.return_value.put.return_value = test_case["response"]
        mock_boto3.return_value = mock_boto3_object

        actual_value = df_to_s3_csv(
            df=test_case["df"],
            bucket_name=test_case["bucket_name"],
            file_name=test_case["file_name"],
        )

        assert actual_value == test_case["response"]

        # TODO - add some other assertions and tests


@pytest.fixture(scope="module")
def df_to_s3_csv_test_exceptions():
    test_cases: typing.List[typing.Any] = [
        # test exception
        {
            "bucket_name": "mybucket",
            "file_name": "myfile",
            "df": pd.DataFrame(
                {"High": [3, 4], "Low": [3, 4]}, index=["01-01-2001", "01-02-2001"],
            ),
            "response": {
                "Expiration": "string",
                "ETag": "string",
                "ServerSideEncryption": "AES256",
                "VersionId": "string",
                "SSECustomerAlgorithm": "string",
                "SSECustomerKeyMD5": "string",
                "SSEKMSKeyId": "string",
                "SSEKMSEncryptionContext": "string",
                "RequestCharged": "requester",
            },
            "mock_side_effect": Exception("Boom!"),
            "expected_exception": StorageError,
        }
    ]
    yield test_cases
    # tear-down


@patch("boto3.resource")
def test_df_to_s3_csv_exception(mock_boto3, df_to_s3_csv_test_exceptions):

    for test_case in df_to_s3_csv_test_exceptions:

        mock_boto3.side_effect = test_case["mock_side_effect"]

        with pytest.raises(Exception) as exception_info:
            actual_value = df_to_s3_csv(
                df=test_case["df"],
                bucket_name=test_case["bucket_name"],
                file_name=test_case["file_name"],
            )

        assert isinstance(exception_info.value, test_case["expected_exception"])
