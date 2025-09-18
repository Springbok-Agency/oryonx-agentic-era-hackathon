
import json
from google.cloud import bigquery
import datetime
def convert_dates(obj):
    """
    Recursively convert date and datetime objects in dicts/lists to ISO strings.
    """
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    else:
        return obj

GCP_PROJECT_ID = "qwiklabs-gcp-03-3444594577c6"
BQ_DATASET = "product_data"
BQ_TABLE = "product_data_table"


def get_product_data(project: str = GCP_PROJECT_ID, dataset: str = BQ_DATASET, table: str = BQ_TABLE, limit: int = 10):
    """Get all product data from BigQuery.

    Args:
        project (str, optional): GCP project ID.
        dataset (str, optional): BigQuery dataset name.
        table (str, optional): BigQuery table name.
        limit (int, optional): Number of records to fetch.

    Returns:
        list[dict]: A list of product data records.
    """

    client = bigquery.Client(project=project)

    query = f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT {limit}"
    query_job = client.query(query)
    results = query_job.result()
    products = [dict(row) for row in results]
    return convert_dates(products)


if __name__ == "__main__":
    print(json.dumps(get_product_data(), indent=4))