import datetime
import json
from typing import Any

from google.cloud import bigquery

GCP_PROJECT_ID = "qwiklabs-gcp-03-3444594577c6"
BQ_DATASET = "product_data"
BQ_TABLE = "product_data_table"


def _serialize_date(obj: Any) -> Any:
    """Convert date objects to ISO format strings for JSON serialization."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def get_product_data(
    project: str = GCP_PROJECT_ID,
    dataset: str = BQ_DATASET,
    table: str = BQ_TABLE,
    limit: int = 5,
) -> str:
    """Get all product data from BigQuery as a JSON string.

    Args:
        project (str, optional): GCP project ID.
        dataset (str, optional): BigQuery dataset name.
        table (str, optional): BigQuery table name.
        limit (int, optional): Number of records to fetch.

    Returns:
        str: A JSON string containing the product data records.
    """

    print("Getting product data")

    client = bigquery.Client(project=project)

    query = f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT {limit}"
    query_job = client.query(query)
    results = query_job.result()

    print("Got results")

    # Convert BigQuery Row objects to dictionaries and serialize dates
    products = []
    for row in results:
        # Convert Row to dict
        row_dict = dict(row)
        # Serialize any date objects
        serialized_row = {k: _serialize_date(v) for k, v in row_dict.items()}
        products.append(serialized_row)

    print("Done getting product data")

    # Convert to JSON string (compact format to avoid function call truncation)
    return json.dumps(products)


if __name__ == "__main__":
    print(get_product_data())
