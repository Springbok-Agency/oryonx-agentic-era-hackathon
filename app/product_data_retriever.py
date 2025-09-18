from google.cloud import bigquery

GCP_PROJECT_ID = "qwiklabs-gcp-03-3444594577c6"
BQ_DATASET = "product_data"
BQ_TABLE = "product_data_table"


def get_product_data(project=GCP_PROJECT_ID, dataset=BQ_DATASET, table=BQ_TABLE, limit=10):
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

    return products
