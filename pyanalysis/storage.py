import pandas as pd
import logging

logger = logging.getLogger(__name__)


def df_to_s3_csv(df: pd.DataFrame, bucket_name: str, file_name: str):
    # save a df to s3 as a csv
    #
    # from io import StringIO
    # import boto3
    # csv_buffer = StringIO()
    # df.to_csv(csv_buffer)
    # s3_resource = boto3.resource('s3')
    # s3_resource.Object(bucket_name, file_name)
    # .put(Body=csv_buffer.getvalue())
    #
    logger.info(
        f"Storing to S3 bucket: {bucket_name}; Object name: {file_name}"
    )
    pass
