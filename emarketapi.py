import asyncio
import aiohttp
# import sys
from prettytable import PrettyTable


URL = 'https://emarket-shop.herokuapp.com/api/products-list'


# if len(sys.argv) > 1:
#     keys = sys.argv[1:]
# else:
#     keys = ['name']


def prettyprint(products, keys):
	table = PrettyTable(keys)
	for product in products:
		vals = []
		for key in keys:
			val = product[key]
			vals.append(val)
		table.add_row(vals)
	print(table)


async def fetch_product_list(keys=['name'], url=URL):
	r = await aiohttp.request('GET', URL)
	products = await r.json()
	r.close()
	prettyprint(products, keys)


async def timer(sec):
	for s in range(sec):
		print(s)
		await asyncio.sleep(1)


def run ():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(fetch_product_list(), timer(3)))
	print('Done')


if __name__ == "__main__":
	run()
