import argparse
import asyncio
import aiohttp
import sys
from prettytable import PrettyTable
from concurrent.futures import FIRST_COMPLETED


URL = 'https://emarket-shop.herokuapp.com/api/products-list'


def prettyprint(products, keys):
    table = PrettyTable(keys)
    for product in products:
        vals = []
        for key in keys:
            val = product[key]
            vals.append(val)
        table.add_row(vals)
    print(table)


async def fetch_product_list():
    # TODO: product parameters should be specified in request
    # not picked on client side.
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as r:
            return await r.json()


async def timer(sec):
    for s in range(sec):
        print(s)
        await asyncio.sleep(1)


async def asyncFetchAndPrint(keys):
    task_fetch = asyncio.ensure_future(fetch_product_list())
    task_timer = asyncio.ensure_future(timer(22))
    tasks = [task_timer, task_fetch]
    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)

    if task_fetch in done:
        products = task_fetch.result()
        prettyprint(products, keys)

    for future in pending:
        future.cancel()


def main(keys):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncFetchAndPrint(keys))
    loop.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        keys = sys.argv[1:]
    else:
        keys = ['name']
    main(keys)
