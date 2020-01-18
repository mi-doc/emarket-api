import asyncio
import aiohttp
import sys
from prettytable import PrettyTable
from concurrent.futures import FIRST_COMPLETED
import json


URL = 'https://emarket-shop.herokuapp.com/api/products-list/'
# URL = 'http://127.0.0.1:8000/api/products-list/'

def prettyprint(products):
    """
    This func creates nice ASCII-based sheet to display data in terminal
    """
    fields_to_show = products[1].keys()
    table = PrettyTable(fields_to_show)
    for product in products:
        vals = [product[key] for key in fields_to_show]
        table.add_row(vals)
    print(table)


async def fetch_product_list(fields_to_show):
    """
    Asynchorously fetching products with specified params from emarket api
    :param fields_to_show: product params required to fetch (name, price, ram etc)
    """
    params = {'q': fields_to_show}
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=params) as r:
            return await r.json()


async def timer(sec=100):
    """
    Prints seconds. It makes no real sense, just playing with asynchronous.
    """
    for s in range(sec):
        print(s)
        await asyncio.sleep(1)


async def main(fields_to_show):
    task_fetch = asyncio.ensure_future(fetch_product_list(fields_to_show))
    task_timer = asyncio.ensure_future(timer())
    tasks = [task_timer, task_fetch]

    while True:
        # Waiting untill products are fetched from emarket.
        done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
        if task_fetch in done:
            break

    # Cancel coroutine with timer.
    for future in pending:
        future.cancel()

    products = task_fetch.result()
    prettyprint(products)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fields_to_show = sys.argv[1:]
    else:
        fields_to_show = ['name']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(fields_to_show))
    loop.close()
