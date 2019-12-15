import asyncio
import aiohttp
from contextlib import closing
# import sys
# import requests
from prettytable import PrettyTable


URL = 'https://emarket-shop.herokuapp.com/api/products-list'

# print('wait... \n')
# r = requests.get(URL)
# products = r.json()
#
# if len(sys.argv) > 1:
#     keys = sys.argv[1:]
# else:
#     keys = ['name']
#
# table = PrettyTable(keys)
# for product in products:
#     vals = []
#     for key in keys:
#         val = product[key]
#         vals.append(val)
#     table.add_row(vals)
# print(table)


# sync def timer(sec):
# for s in range(sec):
# 	print(s)
# 	await asyncio.sleep(1)


def prettyprint(products, keys):
	table = PrettyTable(keys)
	for product in products:
		print(product)
		vals = []
		for key in keys:
			val = product[key]
			vals.append(val)
		table.add_row(vals)
	print(table)


async def fetch_product_list(loop, keys=['name'], url=URL):
	with aiohttp.ClientSession(loop=loop) as session:
		with aiohttp.Timeout(31):
			async with session.get(url) as r:
				assert r.status == 200
				products = await r.json()
				prettyprint(products, keys)


async def timer(sec):
	for s in range(sec):
		print(s)
		await asyncio.sleep(1)


def run ():
	with closing(asyncio.get_event_loop()) as loop:
		loop.run_until_complete(asyncio.gather(fetch_product_list(loop), timer(3)))
	print('Done')


if __name__ == "__main__":
	run()
