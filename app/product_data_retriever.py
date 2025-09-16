def get_product_data(project, dataset, table):
	"""Fetch product data from BigQuery."""
	from google.cloud import bigquery

	client = bigquery.Client(project=project)
	query = f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT 10"
	query_job = client.query(query)
	results = query_job.result()
	products = [dict(row) for row in results]
	return products


project = "qwiklabs-gcp-03-3444594577c6"
dataset = "product_data"
table = "product_data_table"
products = get_product_data(project, dataset, table)
print(products)