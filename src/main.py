"""
Python 3.8.5 64-bit
Author: Adam Turner <turner.adch@gmail.com>
Based on a scrapy spider written by Liam Xiao.
"""
# pypi
import requests
import lxml.html
import sqlalchemy
import numpy as np
import pandas as pd
# standard library
import pathlib
from datetime import datetime
# local
import conndb
from validation import Adjudicator


def sql_send_to_db(engine_info, dataframe):
	"""Appends data to xxxxxxxxxxxxx.xxx_xxxx_xxxx_xxxx table.

	Args:
	dataframe: pd.DataFrame, example final table below
		|  name  | value |        last_updated        |
		| ------ | ----- | -------------------------- |
		| xxxxxx | xx.xx | xxxx-xx-xx xx:xx:xx.xxxxxx |
	"""
	print("Updating database...")
	sql_engine = sqlalchemy.create_engine(engine_info)

	try:
		dataframe.to_sql(
			con=sql_engine, 
			schema='xxxxxxxxxxxxx',
			name='xxx_xxxx_xxxx_xxxx',
			if_exists='append', 
			index=False
		)
	except ValueError as e:
		raise ValueError(f"DataFrame to SQL error: {e}")

	print("Database update complete.")

	return None


def crawl(route, verify):
	"""Crawls along a route and stores http get responses.

	Args:
		route: list containing url strings
		verify: bool, verify ssl certificates

	Returns:
		responses: list of requests Response objects
	"""
	responses = []
	with requests.Session() as s:
		for url in route:
			response = s.get(url, verify=False)
			responses.append(response)
			print(f"Response URL: {response.url}\n  > Status code {response.status_code}")

	return responses


def main():
	src_path = pathlib.Path(__file__).parent.absolute()
	utils_path = src_path.parent / 'utils'

	route = [
		'https://sample.route.wall',
		'https://sample.route.wall.bypass',
		'https://sample.route.target'
	]x
	responses = crawl(route=route, verify=False)

	target = responses[-1]
	if target.url == route[-1]:
		if target.status_code == 200:
			print(f"Valid target url {target.url} with status code {target.status_code}.")
		else:
			raise ValueError(f"{target.url} returned an unexpected status code: {target.status_code}")
	else:
		raise ValueError(f"{route[-1]} was not reached, we ended up at {target.url}")

	# use xpath expression to extract the real time table rows
	html_document = lxml.html.document_fromstring(target.text)
	names = html_document.xpath("//table[@class='xxxxxxxx']//table//tr//div[@class='xxxxxxxx']")
	values = html_document.xpath("//table[@class='xxxxxxxx']//table//tr//div[@class='xxxxx']")

	# validate the data
	if len(names) != len(values):
		raise ValueError(f"List length mismatch: {len(names)} names, {len(values)} values.")
	records = [(name.text.strip(), value.text.strip()) for name, value in zip(names, values)]
	Adjudicator.validate_names([record[0] for record in records])
	Adjudicator.validate_values([record[1] for record in records])

	# pandas magic
	df = pd.DataFrame.from_records(records)
	df.columns = ['name', 'value']
	df['last_updated'] = datetime.now()

	# send data to the database
	config_path = str(utils_path / 'config.properties')
	engine_info = conndb.get_engine_info(config_path)
	# sql_send_to_db(engine_info=engine_info, dataframe=df)
	print("End of main spider program.")

	return None


if __name__ == "__main__":
	main()
